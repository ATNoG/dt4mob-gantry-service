## Scripts & Commands

There is no Makefile or task runner. All commands use `uv` directly:

### Development

```bash
# Install/sync dependencies
uv sync

# Run the service
uv run main.py
```

### Type Checking

```bash
uv run mypy
```

Runs mypy in strict mode with the pydantic plugin. Configuration is in `pyproject.toml` under `[tool.mypy]`.

### Linting

```bash
uv run ruff check
```

Runs ruff with print-statement detection (T20 rule). Configuration is in `pyproject.toml` under `[tool.ruff]`.

### Docker

```bash
# Build and run
docker compose up --build

# Run in background
docker compose up --build -d

# Stop
docker compose down
```
