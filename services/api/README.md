# API Service

One endpoint returning a small JSON response. The router is in `api.py` and is
served by `services/main.py`.

- Hostname: `api.internal.local`
- HTTP: port 8082. HTTPS: port 8444.
- Endpoint: `GET /health`

Start (from the repository root):

```
python -m services.main api --mode http
python -m services.main api --mode https
```

See [`services/README.md`](../README.md) for setup, certificates,
verification commands, and expected responses.
