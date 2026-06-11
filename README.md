# Gantry Service

## Configuration Architecture

You can configure the bridge using two primary methods:

1. **`config.toml`**: The service looks for this file in the root directory by default.
2. **Environment Variables**: Use the prefix `GS_`. For nested attributes, use a double underscore `__`.

- _Example_: `GS_SENDER__HOST="10.0.0.1"` maps to `sender.host`.

3. **Logging**: Control the verbosity via `log_level` (Options: `TRACE`, `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).

---

## Inbound: Consumers

Consumers define how the bridge ingests data. You can configure multiple consumers simultaneously in a list.

### 1. MQTT Consumer

- **Backend**: `mqtt`.
- **Connection**: Supports `host`, `port` (default `1883`), and optional authentication (`username`/`password`).
- **Security**: Can be toggled to `secure` mode, which automatically adjusts the connection URI to `mqtts://`.

### 2. Webhook Consumer

- **Backend**: `webhook`.
- **Connection**: Listens on a specified `host` and `port` (default `8000`) for incoming HTTP data.

---

## Message Logic & Validation

Every consumer handles a list of `message_settings`. This is where you define the "rules of engagement" for specific data streams.

| Setting             | OutSight Message                            | AToBe Message                                        |
| ------------------- | ------------------------------------------- | ---------------------------------------------------- |
| **Discriminator**   | `expected_message_type: "outsight"`         | `expected_message_type: "a-to-be"`                   |
| **Source Identity** | Requires `source_name` and `source_prefix`. | Requires `source_name` and `source_prefix`.          |
| **Topic**           | Defined `topic` for routing.                | Defined `topic` for routing.                         |
| **Specifics**       | N/A                                         | Must specify `atobe_type` (`realtime` or `history`). |
| **Formats**         | Defines `allowed_ditto_formats`.            | Defines `allowed_ditto_formats`.                     |

---

## The Processing Pipeline

Before data reaches the sender, it passes through two optional layers:

### Message Converters

This is a toggle-based system to enable or disable specific transformation logic.

- **Available Backends**: `a-to-be`, `outsight`.
- **Configuration**: Set to `true` or `false` in a dictionary format.

### Envelope Formatters

Defines how the final message is wrapped before delivery.

- **Available Backends**: `toll-feature`, `ditto-thing`.

---

## Outbound: Senders

The `sender` defines the final destination of the telemetry. While you can have multiple consumers, only **one** sender backend is active at a time.

- **MQTT Sender**:
- Constructs a URI based on `host`, `port`, and `tls` status.
- Supports `cafile` for secure connections.
- Publishes to a configurable `publish_topic`.

- **HTTP Sender**:
- Sends data to a `base_path` (default `/telemetry`).
- Full support for `tls`, `client_key`, and `client_crt` for mutual TLS (mTLS).

- **Disabled**: The default state; no data is sent outbound.

---

## Integration Modules

### Toll Loader

A specialized module for loading tolling-specific metadata.

- **`json-file`**: Points to a local `.json` file (default `tolls.json`).
- **`disabled`**: No external metadata is loaded.

### Ditto Integration

Configures metadata for integration with Eclipse Ditto digital twins.

- **Fields**: `toll_id` (Non-negative integer), `namespace`, `subject`, and `policy_id`.

## More information

Please look at the [example configuration file](./example.config.toml) for all available options and
default values.
