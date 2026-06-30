## Deployment

### Docker Build

The `Dockerfile` uses a multi-step approach:

1. Base image: `python:3.13-slim`
2. Copies `uv` from the official Astral image
3. Copies `pyproject.toml`, `uv.lock`, `.python-version` first (for layer caching)
4. Runs `uv sync --frozen --no-cache` to install dependencies
5. Copies application code
6. Entry command: `uv run main.py`

### Production Deployment

```bash
# Build the image
docker compose build

# Deploy (with detached mode)
docker compose up -d

# View logs
docker compose logs -f gantry-service

# Stop
docker compose down
```

Ensure all the files are available at runtime:
