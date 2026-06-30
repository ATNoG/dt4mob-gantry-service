## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/ATNoG/dt4mob-gantry-service.git
cd dt4mob-gantry-service
```

### 2. Install uv (if not installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Install dependencies

```bash
uv sync
```

This installs both runtime and dev dependencies (mypy, ruff) into a virtual environment.

### 4. Configure the service

```bash
cp config.example.toml config.toml
```

Edit `config.toml` with your local settings. At minimum, configure:

- `[ditto]` identity settings
- At least one `[[consumers]]` block
- Corresponding `[[consumers.message_settings]]` entries
- `[sender]` backend pointing to your Hono/MQTT instance
- `[message_converters]` and `[envelope_formatters]` for your pipeline

### 5. Set up tolls data (optional)

```bash
cp tolls.example.json tolls.json
```

Edit `tolls.json` with your toll gantry definitions.

### 6. Run

```bash
uv run main.py
```

### Environment Variables

Settings can be overridden via environment variables using the `GS_` prefix with `__` as the nested delimiter:

```bash
export GS_LOG_LEVEL="DEBUG"
export GS_SENDER__HOST="10.0.0.1"
export GS_SENDER__MQTT__PORT=1884
export GS_DITTO__NAMESPACE="gantries"
```

The priority order is: environment variables → `config.toml` values.
