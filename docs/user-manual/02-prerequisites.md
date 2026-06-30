## Prerequisites

Before using the Gantry Service, ensure you have:

- **Python 3.13+** installed (check with `python --version`)
- **[uv](https://docs.astral.sh/uv/)** package manager installed (Visit <https://docs.astral.sh/uv/getting-started/installation/> to install)
- **Docker** and **Docker Compose** (if running via containers)
- **An MQTT broker** accessible (e.g., Mosquitto) if using MQTT consumers or sender
- **Eclipse Hono** instance accessible if sending via MQTT
- **A CA certificate file** (`ca.crt`) for TLS connections to your Hono/MQTT broker, placed in the project's parent directory
