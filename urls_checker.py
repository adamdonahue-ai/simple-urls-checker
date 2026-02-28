#!/usr/bin/env python3
"""
urls-checker: URL health checker with retries and streaming output.

Requires Python 3.13.

Usage:
    urls-checker \
        --urls-file FILE
        --timeout SECONDS
        --retries COUNT
        --valid-status-codes LIST_OF_CODES
        --concurrency NUMBER
"""

import argparse
import asyncio
import http
import sys
import typing

import aiohttp


def comma_separated_status_codes(value: str) -> set[int]:
    """
    Custom parameter to ensure value is a comma-separated list
    of valid HTTP status codes.
    """
    valid_status_codes = {status.value for status in http.HTTPStatus}
    result = set()
    for code in value.split(","):
        try:
            code_i = int(code)
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"Invalid status code: {code!r}. "
                "Expected comma-separated integer HTTP status codes."
            )
        if code_i not in valid_status_codes:
            raise argparse.ArgumentTypeError(
                f"{code_i} is not a valid HTTP status code."
            )
        result.add(code_i)
    return result


def parse_args():
    parser = argparse.ArgumentParser(
        prog="urls-checker",
        description=(
            "Check health of URLs from a file with concurrency and retries."
        ),
    )
    parser.add_argument(
        "--urls-file",
        type=argparse.FileType("r"),
        default=sys.stdin,
        nargs="?",
        help="Path to file containing URLs (one per line).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Timeout in seconds per request (default: 5).",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Number of retry attempts (default: 3).",
    )
    parser.add_argument(
        "--valid-status-codes",
        type=comma_separated_status_codes,
        default="200",
        help="Comma-separated list of healthy status codes (default: 200).",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=20,
        help="Max concurrent requests (default: 20).",
    )
    return parser.parse_args()


def format_result(url: str, ok: bool, status: str, retries: int) -> str:
    return f"{'OK' if ok else 'ERROR':<5}  {url}  [{status}]  retries={retries}"


async def worker(
    session: aiohttp.ClientSession,
    queue: asyncio.Queue[str],
    timeout: float,
    max_retries: int,
    valid_status_codes: set[int],
) -> None:
    client_timeout = aiohttp.ClientTimeout(total=timeout)

    while True:
        url = await queue.get()
        try:
            attempt = 0
            last_error = None

            while attempt <= max_retries:
                try:
                    async with session.head(
                        url,
                        timeout=client_timeout,
                        allow_redirects=True,
                    ) as resp:
                        if resp.status in valid_status_codes:
                            print(
                                format_result(
                                    url,
                                    ok=True,
                                    status=str(resp.status),
                                    retries=attempt,
                                ),
                                # Print results as they are determined.
                                flush=True,
                            )
                            break
                        else:
                            last_error = f"HTTP {resp.status}"
                except asyncio.TimeoutError:
                    last_error = "Timeout"
                except aiohttp.ClientError as e:
                    last_error = str(e)
                except Exception as e:
                    last_error = f"Unexpected: {e}"

                attempt += 1
            else:
                print(
                    format_result(
                        url,
                        ok=False,
                        status=last_error or "unknown error",
                        retries=attempt - 1,
                    ),
                    flush=True,
                )
        finally:
            queue.task_done()


async def producer(
    urls_file: typing.IO[str], queue: asyncio.Queue[str]
) -> None:
    for line in urls_file:
        url = line.strip()
        if not url or url.startswith("#"):
            continue
        await queue.put(url)


async def run(
    urls_file: typing.IO[str],
    timeout: float,
    retries: int,
    valid_status_codes: set[int],
    concurrency: int,
) -> None:
    queue: asyncio.Queue[str] = asyncio.Queue(maxsize=concurrency * 2)

    async with aiohttp.ClientSession(
        headers={"User-Agent": "Mozilla/5.0"},
        # Accommodate for larger headers.
        max_line_size=16384,
        max_field_size=16384,
    ) as session:
        workers = [
            asyncio.create_task(
                worker(
                    session, queue, timeout, retries, valid_status_codes
                )
            )
            for _ in range(concurrency)
        ]

        await producer(urls_file, queue)
        await queue.join()

        for w in workers:
            w.cancel()

        # We might in the future use asycnio.wait for more control
        # over when the checker might fail or to inspect the tasks
        # themselves, but this is a quick implementation for interview
        # purposes.
        await asyncio.gather(*workers, return_exceptions=True)


async def main():
    args = parse_args()
    await run(
        args.urls_file,
        args.timeout,
        args.retries,
        args.valid_status_codes,
        args.concurrency,
    )


if __name__ == "__main__":
    asyncio.run(main())
