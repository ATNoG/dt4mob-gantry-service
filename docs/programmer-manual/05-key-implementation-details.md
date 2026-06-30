## Key Implementation Details

### Consumer Drivers

- **MQTT Consumer** (`app/drivers/consumer/mqtt/consumer.py`): Uses `amqtt.client.MQTTClient` with `ClientConfig` and `ConnectionConfig`. Subscribes to all configured topics at QOS 0. Message topic → `message_settings` lookup is done by matching the MQTT topic string.

- **Webhook Consumer** (`app/drivers/consumer/webhook/consumer.py`): Creates a `FastAPI` app with a catch-all POST endpoint `/{topic:path}`. Runs via `uvicorn.Server`. Only processes topics present in the configured `message_settings`.

### Message Converters

- **AToBe** (`app/drivers/message_converter/a_to_be/message_converter.py`): Handles `realtime` (→ `VehicleDataMessage`) and `history` (→ `VehicleDeleteMessage`) sub-types. Validates incoming messages against Pydantic schemas.

- **OutSight** (`app/drivers/message_converter/outsight/message_converter.py`): Uses a `set` to track seen message IDs. Handles out-of-order delivery: first-seen messages are queued; re-received messages with `out_alert` produce final `VehicleDataMessage`.

### Envelope Formatters

- **Toll Feature** (`app/drivers/envelope_formatter/toll_feature/envelope_formatter.py`): Single Ditto thing per toll with per-sensor features. Uses a rolling buffer (size 50) for vehicle IDs; older entries get `delete` commands. `delete_all()` wipes all source features.

- **Ditto Thing** (`app/drivers/envelope_formatter/ditto_thing/envelope_formatter.py`): Separate Ditto thing per vehicle. Uses `deferred_creation_offset` to create "future things" that expire automatically. Generates `create`, `modify`, and expiry commands.

### Sender Drivers

- **MQTT Sender** (`app/drivers/sender/mqtt/sender.py`): Publishes to Eclipse Hono via `amqtt`. Supports TLS with CA certificate. Uses `reconnect_retries=-1` for infinite reconnection.

- **HTTP Sender** (`app/drivers/sender/http/sender.py`): Posts JSON via `httpx.AsyncClient`. Supports basic auth and mTLS with client certificates.
