FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


WORKDIR /app
COPY pyproject.toml uv.lock .python-version /app/

RUN uv sync --frozen --no-cache;

COPY . .

CMD ["uv", "run", "main.py"]

