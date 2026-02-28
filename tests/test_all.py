"""
Unit tests for urls-checker application.
"""

import argparse
import asyncio
import io

import pytest

from aioresponses import aioresponses as mock_aioresponses

from urls_checker import (
    comma_separated_status_codes,
    format_result,
    producer,
    run,
)


class TestCommaSeperatedStatusCodes:
    def test_single_valid_code(self):
        assert comma_separated_status_codes("200") == {200}

    def test_multiple_valid_codes(self):
        assert comma_separated_status_codes("200,201,404") == {
            200,
            201,
            404,
        }

    def test_whitespace_is_stripped(self):
        assert comma_separated_status_codes("200, 201 , 404") == {
            200,
            201,
            404,
        }

    def test_invalid_non_integer_raises(self):
        with pytest.raises(
            argparse.ArgumentTypeError, match="Invalid status code"
        ):
            comma_separated_status_codes("abc")

    def test_invalid_http_code_raises(self):
        with pytest.raises(
            argparse.ArgumentTypeError,
            match="not a valid HTTP status code",
        ):
            comma_separated_status_codes("999")

    def test_mixed_valid_and_invalid_raises(self):
        with pytest.raises(argparse.ArgumentTypeError):
            comma_separated_status_codes("200,999")


class TestFormatResult:
    def test_ok_result(self):
        result = format_result(
            "https://example.com", ok=True, status="200", retries=0
        )
        assert result.startswith("OK")
        assert "200" in result
        assert "retries=0" in result

    def test_error_result(self):
        result = format_result(
            "https://example.com",
            ok=False,
            status="HTTP 503",
            retries=3,
        )
        assert result.startswith("ERROR")
        assert "503" in result
        assert "retries=3" in result

    def test_ok_field_is_padded(self):
        result = format_result(
            "https://example.com", ok=True, status="200", retries=0
        )
        assert result.startswith("OK   ") or result.startswith("OK  ")

    def test_error_field_not_padded(self):
        result = format_result(
            "https://example.com", ok=False, status="timeout", retries=1
        )
        assert result.startswith("ERROR")


class TestProducer:
    async def test_enqueues_urls(self):
        urls = "https://example.com\nhttps://other.com\n"
        queue = asyncio.Queue()
        await producer(io.StringIO(urls), queue)
        assert queue.qsize() == 2
        assert await queue.get() == "https://example.com"
        assert await queue.get() == "https://other.com"

    async def test_skips_blank_lines(self):
        urls = "https://example.com\n\nhttps://other.com\n"
        queue = asyncio.Queue()
        await producer(io.StringIO(urls), queue)
        assert queue.qsize() == 2

    async def test_skips_comments(self):
        urls = "# this is a comment\nhttps://example.com\n"
        queue = asyncio.Queue()
        await producer(io.StringIO(urls), queue)
        assert queue.qsize() == 1
        assert await queue.get() == "https://example.com"

    async def test_empty_file(self):
        queue = asyncio.Queue()
        await producer(io.StringIO(""), queue)
        assert queue.qsize() == 0


class TestWorker:
    async def test_successful_request(self, capsys):
        with mock_aioresponses() as m:
            m.get("https://example.com", status=200)
            await run(
                io.StringIO("https://example.com\n"),
                timeout=5.0,
                retries=0,
                valid_status_codes={200},
                concurrency=1,
            )
        assert "OK" in capsys.readouterr().out

    async def test_failed_request_exhausts_retries(self, capsys):
        with mock_aioresponses() as m:
            for _ in range(4):
                m.get("https://example.com", status=503)
            await run(
                io.StringIO("https://example.com\n"),
                timeout=5.0,
                retries=3,
                valid_status_codes={200},
                concurrency=1,
            )
        captured = capsys.readouterr()
        assert "ERROR" in captured.out
        assert "retries=3" in captured.out

    async def test_timeout_is_retried(self, capsys):
        with mock_aioresponses() as m:
            for _ in range(4):
                m.get(
                    "https://example.com",
                    exception=asyncio.TimeoutError(),
                )
            await run(
                io.StringIO("https://example.com\n"),
                timeout=5.0,
                retries=3,
                valid_status_codes={200},
                concurrency=1,
            )
        captured = capsys.readouterr()
        assert "ERROR" in captured.out
        assert "Timeout" in captured.out

    async def test_retry_succeeds_on_second_attempt(self, capsys):
        with mock_aioresponses() as m:
            m.get("https://example.com", status=503)
            m.get("https://example.com", status=200)
            await run(
                io.StringIO("https://example.com\n"),
                timeout=5.0,
                retries=3,
                valid_status_codes={200},
                concurrency=1,
            )
        captured = capsys.readouterr()
        assert "OK" in captured.out
        assert "retries=1" in captured.out
