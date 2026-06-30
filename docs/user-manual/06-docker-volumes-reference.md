## Docker Volumes Reference

When running via Docker Compose, the following volumes are mounted:

| Host Path       | Container Path     | Mode      | Purpose                            |
| --------------- | ------------------ | --------- | ---------------------------------- |
| `./config.toml` | `/app/config.toml` | read-only | Service configuration              |
| `./ca.crt`      | `/app/ca.crt`      | read-only | CA certificate for TLS connections |

Port `8000` is exposed for the webhook consumer endpoint.

To add additional volumes (e.g., for custom tolls data or certificates), add entries to the `volumes` section in `compose.yml`.
