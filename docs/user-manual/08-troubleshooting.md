## Troubleshooting

### Service won't start

- Verify `config.toml` exists in the project root and is valid TOML
- Change the `log_level` to `DEBUG` or `TRACE` for verbose output
- Ensure all certificate and key files (e.g., `ca.crt`, `crt.pem`, `key.pem`) are present at the path specified in your configuration

### Messages not appearing in Ditto

- Confirm that at least one of each component is enabled and configured
- Verify the MQTT/HTTP sender connection details (host, port, credentials) are correct
- Check that the CA certificate path is correct and the file is readable
- Ensure the toll loader is configured if your envelope formatter requires toll metadata

### Webhook consumer not receiving data

- Confirm the webhook consumer port (default `8000`) is not blocked by a firewall
- Verify the POST request URL matches the configured `topic` field
- Check that `expected_message_type` and `source_name` are set in the corresponding `message_settings`

### Stale data in Ditto

- The clear loop runs every 150 seconds by default; adjust `clear_loop_interval_s` if you need faster cleanup
- The toll-feature formatter keeps a rolling buffer of 50 vehicle IDs per sensor; older entries are automatically deleted
