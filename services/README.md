# Internal Services (Wiki and API)

Two small FastAPI services used for the HTTP baseline and the HTTPS demo.
They run as separate processes on separate ports so they can be tested
independently.

## Setup

Requires Python 3.9+.

```
pip install fastapi uvicorn
```

Add this line to `/etc/hosts` (WSL/Linux). If you also test from Windows, add
it to `C:\Windows\System32\drivers\etc\hosts`:

```
127.0.0.1  wiki.internal.local  api.internal.local
```

## Hostnames and ports

| Service | Hostname | HTTP port | HTTPS port |
|---|---|---|---|
| Wiki | wiki.internal.local | 8080 | 8443 |
| API | api.internal.local | 8082 | 8444 |

Ports used by the security tests (not by these services): 8081 (fake HTTP wiki),
9443 (fake HTTPS wiki), 9444 (unrelated-CA HTTPS test).

## Start and stop

Run all commands from the **repository root**. Use one terminal per service.
Stop any service with `Ctrl+C`.

| Service | Mode | Command |
|---|---|---|
| Wiki | HTTP | `python -m services.main wiki --mode http` |
| API | HTTP | `python -m services.main api --mode http` |
| Wiki | HTTPS | `python -m services.main wiki --mode https` |
| API | HTTPS | `python -m services.main api --mode https` |

By default services bind to `127.0.0.1`. To bind to another interface (for
example a VM address), set `BIND_HOST`:

```
BIND_HOST=0.0.0.0 python -m services.main wiki --mode http
```

Only expose the services inside the authorized lab environment.

## Expected responses

**Wiki** (`/`): an HTML page titled "Internal Organizational Wiki" with a
security notice. In HTTP mode it says "HTTP Baseline" and "plain unencrypted
HTTP". In HTTPS mode it says "HTTPS".

**API** (`/health`): a small JSON response.

```json
{"status": "healthy", "service": "internal-api", "version": "1.0", "mode": "HTTP"}
```

`mode` is `HTTP` or `HTTPS` depending on how the service was started.

## HTTP baseline

```
curl http://wiki.internal.local:8080/
curl http://api.internal.local:8082/health
```

HTTP does not provide TLS encryption or cryptographic server identity
verification. Anyone on the network path can read or modify the traffic, and a
client has no way to prove it is talking to the real server. This is the
deliberately vulnerable baseline for the demo.

## HTTPS

Each service loads only its own certificate and key, issued by the internal
Root CA. The certificate for each service must include its hostname in the SAN
(`wiki.internal.local` or `api.internal.local`).

| Service | Certificate | Private key |
|---|---|---|
| Wiki | `certificates/wiki.crt` | `certificates/wiki.key` |
| API | `certificates/api.crt` | `certificates/api.key` |

To use a different directory, set `CERT_DIR`:

```
CERT_DIR=/path/to/certs python -m services.main wiki --mode https
```

**Private keys are never committed.** `.gitignore` blocks `*.key` and `*.pem`.
Get keys from Member 1 privately or generate them locally.

### Verify HTTPS

Use the Root CA for trust. Do not use `curl -k` or `--insecure`.

```
curl --cacert rootCA.crt https://wiki.internal.local:8443/
curl --cacert rootCA.crt https://api.internal.local:8444/health

openssl s_client -connect wiki.internal.local:8443 \
  -servername wiki.internal.local -CAfile rootCA.crt \
  -verify_hostname wiki.internal.local -verify_return_error
```

Repeat the `openssl` check for the API with `api.internal.local:8444`. These
succeed only when the Root CA is trusted, the server presents the correct
certificate, and the hostname matches the SAN.

## Attack demo (for Member 3)

Start both legitimate services in HTTPS mode, one per terminal:

```
python -m services.main wiki --mode https
python -m services.main api --mode https
```

The legitimate wiki (8443) should succeed with `--cacert rootCA.crt`, while the
fake HTTPS wiki (9443) and the unrelated-CA test (9444) should fail
verification. For the HTTP baseline part of the demo, start the services with
`--mode http` instead.
