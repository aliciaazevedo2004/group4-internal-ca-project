# Wiki Service

A single HTML page identifying the service as the internal wiki. The router is
in `wiki.py` and is served by `services/main.py`.

- Hostname: `wiki.internal.local`
- HTTP: port 8080. HTTPS: port 8443.
- Endpoint: `GET /`

Start (from the repository root):

```
python -m services.main wiki --mode http
python -m services.main wiki --mode https
```

See [`services/README.md`](../README.md) for setup, certificates,
verification commands, and expected responses.
