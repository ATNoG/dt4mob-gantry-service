## Project Structure

| Path                    | Description                                                                                                                                                       |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `main.py`               | Application entry point — creates and runs the `BridgeService`                                                                                                    |
| `app/`                  | Application package root                                                                                                                                          |
| `app/interface/`        | Abstract base classes defining the programming interface for the bridge service's pluggable components (consumers, senders, converters, formatters, toll loaders) |
| `app/drivers/`          | Concrete driver implementations for each interface (MQTT/webhook consumers, MQTT/HTTP senders, etc.)                                                              |
| `app/schema/`           | Pydantic data models for Ditto protocol envelopes, vehicle messages, toll definitions, and common types                                                           |
| `app/settings/`         | Pydantic-settings configuration models mapping `config.toml` sections to typed Python objects                                                                     |
| `app/bridge_service.py` | Core orchestration — wires together consumers, converters, formatters, and the sender into an async processing pipeline                                           |
| `config.example.toml`   | Documented example configuration with all available options                                                                                                       |
| `tolls.example.json`    | Example toll definitions file showing the expected JSON schema                                                                                                    |
| `compose.yml`           | Docker Compose service definition for containerised deployment                                                                                                    |
| `Dockerfile`            | Container image build instructions (Python 3.13-slim + uv)                                                                                                        |
| `pyproject.toml`        | Project metadata, dependencies, and tool configuration (mypy, ruff)                                                                                               |
| `docs/`                 | Documentation sources (user manual, programmer manual, build scripts)                                                                                             |
