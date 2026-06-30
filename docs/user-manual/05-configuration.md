## Configuration

Configuration is managed through `config.toml`. Environment variables can override any setting using the `GS_` prefix with `__` as the nested delimiter (e.g., `GS_SENDER__HOST=10.0.0.1`).

### Global Settings

| Field                   | Type           | Default  | Description                                                                          |
| ----------------------- | -------------- | -------- | ------------------------------------------------------------------------------------ |
| `log_level`             | string         | `"INFO"` | Logging verbosity. Options: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`, `TRACE` |
| `clear_loop_interval_s` | positive float | `150`    | Seconds between periodic Ditto cleanup sweeps                                        |

### `[ditto]` — Ditto Identity Settings

| Field       | Type             | Default            | Description                                          |
| ----------- | ---------------- | ------------------ | ---------------------------------------------------- |
| `toll_id`   | non-negative int | `0`                | Numeric identifier for the toll gantry in Ditto      |
| `namespace` | string           | `"default"`        | Ditto namespace for the thing                        |
| `subject`   | string           | `"test"`           | Ditto subject used in the thingId for access control |
| `policy_id` | string           | `"default:policy"` | Ditto policy ID for created things                   |

### `[message_converters]` — Enabled Converters

| Field      | Type | Default | Description                              |
| ---------- | ---- | ------- | ---------------------------------------- |
| `a-to-be`  | bool | `false` | Enable the A-to-Be ORT message converter |
| `outsight` | bool | `false` | Enable the OutSight message converter    |

### `[envelope_formatters]` — Enabled Formatters

| Field          | Type | Default | Description                                                            |
| -------------- | ---- | ------- | ---------------------------------------------------------------------- |
| `toll-feature` | bool | `false` | Enable the toll-feature envelope formatter (single thing per toll)     |
| `ditto-thing`  | bool | `false` | Enable the ditto-thing envelope formatter (separate thing per vehicle) |

### `[ditto_thing_settings]` — Ditto Thing Formatter Options

| Field                      | Type | Default | Description                                                                          |
| -------------------------- | ---- | ------- | ------------------------------------------------------------------------------------ |
| `deferred_creation_offset` | int  | `10`    | Offset added to vehicle IDs for deferred thing creation in the ditto-thing formatter |

### `[toll_loader]` — Toll Metadata Loading

| Field      | Type   | Default        | Description                                                           |
| ---------- | ------ | -------------- | --------------------------------------------------------------------- |
| `backend`  | string | `"disabled"`   | Toll loader backend. Options: `"disabled"`, `"json-file"`             |
| `filepath` | path   | `"tolls.json"` | Path to the JSON tolls file (only used when backend is `"json-file"`) |

**Tolls JSON format:**

```json
{
  "tolls": [
    {
      "id": 1,
      "coords": { "latitude": 38.0, "longitude": -9.0 },
      "name": "Ocean Gantry",
      "sensors": ["camera", "lidar"],
      "dashboardUrl": "https://example.com/grafana/gantry"
    }
  ]
}
```

### `[sender]` — Outbound Sender

| Field     | Type   | Default      | Description                                               |
| --------- | ------ | ------------ | --------------------------------------------------------- |
| `backend` | string | `"disabled"` | Sender backend. Options: `"disabled"`, `"mqtt"`, `"http"` |

#### MQTT Sender (`[sender].backend = "mqtt"`)

| Field           | Type   | Default       | Description                                      |
| --------------- | ------ | ------------- | ------------------------------------------------ |
| `host`          | string | `"localhost"` | MQTT broker hostname                             |
| `port`          | int    | `1883`        | MQTT broker port                                 |
| `username`      | string | —             | MQTT username                                    |
| `password`      | string | —             | MQTT password                                    |
| `tls`           | bool   | `true`        | Enable TLS for the connection                    |
| `cafile`        | string | —             | Path to CA certificate file for TLS verification |
| `certfile`      | string | —             | Path to client certificate for mTLS              |
| `keyfile`       | string | —             | Path to client private key for mTLS              |
| `publish_topic` | string | `"telemetry"` | MQTT topic to publish Ditto envelopes to         |

#### HTTP Sender (`[sender].backend = "http"`)

| Field        | Type   | Default | Description                                      |
| ------------ | ------ | ------- | ------------------------------------------------ |
| `host`       | string | —       | Target HTTP endpoint hostname                    |
| `port`       | int    | `443`   | Target HTTP endpoint port                        |
| `username`   | string | —       | Basic auth username (optional)                   |
| `password`   | string | —       | Basic auth password (optional)                   |
| `tls`        | bool   | `false` | Enable TLS for the connection                    |
| `cafile`     | string | —       | Path to CA certificate file for TLS verification |
| `client_key` | string | —       | Path to client private key for mTLS              |
| `client_crt` | string | —       | Path to client certificate for mTLS              |
| `base_path`  | string | —       | HTTP path to POST JSON payloads to               |

### `[[consumers]]` — Inbound Consumers

Each `[[consumers]]` block defines a sensor data source. You can define multiple consumers.

| Field      | Type   | Default | Description                                      |
| ---------- | ------ | ------- | ------------------------------------------------ |
| `backend`  | string | —       | Consumer backend. Options: `"mqtt"`, `"webhook"` |
| `enabled`  | bool   | `true`  | Whether this consumer is active                  |
| `host`     | string | —       | MQTT broker or webhook listen hostname           |
| `port`     | int    | —       | MQTT broker port or webhook listen port          |
| `secure`   | bool   | `false` | Use TLS for MQTT connection                      |
| `username` | string | —       | MQTT username                                    |
| `password` | string | —       | MQTT password                                    |

#### Consumer Message Settings (`[[consumers.message_settings]]`)

Each consumer can have multiple message settings blocks defining what topics it handles.

| Field                   | Type             | Default | Description                                                                                      |
| ----------------------- | ---------------- | ------- | ------------------------------------------------------------------------------------------------ |
| `expected_message_type` | string           | —       | Sensor format: `"a-to-be"` or `"outsight"`                                                       |
| `topic`                 | non-empty string | —       | MQTT topic to subscribe to, or webhook URL path segment                                          |
| `source_name`           | non-empty string | —       | Identifier for this sensor source (used in Ditto feature paths)                                  |
| `allowed_ditto_formats` | set of strings   | `[]`    | Which envelope formatters to use. Options: `"toll-feature"`, `"ditto-thing"`                     |
| `atobe_type`            | string           | —       | A-to-Be sub-type: `"realtime"` or `"history"` (only when `expected_message_type` is `"a-to-be"`) |

### Example Configuration

```toml
log_level = "INFO"

[ditto]
namespace = "tolls"
policy_id = "dt4mob:default"
toll_id = 1

[[consumers]]
backend = "mqtt"
host = "localhost"
username = "sensor_user"
password = "secret"

[[consumers.message_settings]]
topic = "vehicle/realtime-tracking"
source_name = "camera-ORT"
expected_message_type = "a-to-be"
atobe_type = "realtime"
allowed_ditto_formats = ["toll-feature", "ditto-thing"]

[toll_loader]
backend = "json-file"
filepath = "tolls.json"

[message_converters]
a-to-be = true

[envelope_formatters]
toll-feature = true

[sender]
backend = "mqtt"
host = "hono.example.com"
port = 31918
tls = true
cafile = "../ca.crt"
username = "tolls@hono"
password = "secret"
```
