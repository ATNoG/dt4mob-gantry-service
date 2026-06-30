## Usage Guide

### Starting the Service

Once started, the service will:

1. Load toll metadata from `tolls.json` (if configured) and register toll things in Ditto
2. Connect to all enabled consumers (MQTT brokers or start webhook endpoints)
3. Begin listening for sensor messages
4. Convert incoming messages, wrap them in Ditto envelopes, and send them to your configured backend

### Processing Pipeline

The service processes messages through four stages:

```
Sensors → Consumer → Message Converter → Envelope Formatter → Sender
```

1. **Consumer** receives raw sensor data via MQTT subscription or HTTP webhook POST
2. **Message Converter** normalizes vendor-specific formats into a standard internal format
3. **Envelope Formatter** wraps the normalized data into Eclipse Ditto protocol envelopes
4. **Sender** delivers the envelopes to Eclipse Hono via MQTT or an HTTP endpoint

### Supported Sensor Formats

| Format       | Description                                      | Message Types                                                  |
| ------------ | ------------------------------------------------ | -------------------------------------------------------------- |
| **a-to-be**  | ORT tracking data format from cameras and LiDARs | `realtime` (live detections), `history` (historical path data) |
| **outsight** | OutSight sensor data with alert-based detection  | Alert in/out events with bounding coordinates                  |

### Supported Ditto Envelope Formats

| Format           | Description                                                                                                                                                                                                                      |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **toll-feature** | Creates a single Ditto thing per toll with per-sensor features. Vehicle data is stored under `/features/{source_name}/properties/{vehicle_id}`. Includes rolling cleanup (max 50 vehicles per sensor) and periodic full cleanup. |
| **ditto-thing**  | Creates a separate Ditto thing per detected vehicle with deferred creation. Each vehicle gets its own thing with State features. Includes automatic expiry management.                                                           |

### Clear Loop

The service periodically sends delete commands to wipe all sensor data from Ditto things to prevent stale entries from accumulating and exceeding the maximum thing size. This runs every 150 seconds by default (configurable via `clear_loop_interval_s`).
