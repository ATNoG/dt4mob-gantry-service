## Installation

**Option A: Run Directly with uv**

```bash
# Clone the repository
git clone https://github.com/ATNoG/dt4mob-gantry-service.git
cd dt4mob-gantry-service

# Install dependencies
uv sync

# Copy and edit the example configuration
cp config.example.toml config.toml
# Edit config.toml with your settings (see Configuration section)

# Copy tolls data (if using toll loader)
cp tolls.example.json tolls.json

# Run the service
uv run main.py
```

**Option B: Run with Docker Compose**

```bash
# Clone the repository
git clone https://github.com/ATNoG/dt4mob-gantry-service.git
cd dt4mob-gantry-service

# Copy and edit the example configuration
cp config.example.toml config.toml
# Edit config.toml with your settings (see Configuration section)

# Copy tolls data (if using toll loader)
cp tolls.example.json tolls.json

# Edit the compose.yml file to your needs and run this to build and start
docker compose up --build
```

The available Docker Compose setup automatically:

- Mounts `config.toml` as a read-only volume at `/app/config.toml`
- Mounts `ca.crt` as a read-only volume at `/app/ca.crt` (for TLS)
- Mounts `tolls.json` as a read-only volume at `/app/tolls.json`
- Exposes port `8000` (used by the webhook consumer)
- Maps `host.docker.internal` to the host gateway for local broker access
