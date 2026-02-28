FROM python:3.13-slim AS builder
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /app/.venv ./.venv
COPY urls_checker.py urls-checker.py
ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT ["python", "urls-checker.py"]
