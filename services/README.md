# Internal Services (Wiki and API)

Two small FastAPI services used for the HTTP baseline and the HTTPS demo.
They run as separate processes on separate ports so they can be started and
tested independently. Each service can run in HTTP mode (the deliberately
insecure baseline) or HTTPS mode (using certificates issued by the project's
internal Root CA).

## Quick start

Run all commands from the **repository root**.

```bash
pip install fastapi uvicorn
bash ca/generate-certs.sh                 # type REPLACE when prompted
echo "127.0.0.1 wiki.internal.local api.internal.local" | sudo tee -a /etc/hosts
python -m services.main wiki --mode https
python -m services.main api --mode https   # in a second terminal
```

Requires Python 3.9+ and OpenSSL.

## Hostnames and ports

| Service | Hostname | HTTP port | HTTPS port |
|---|---|---|---|
| Wiki | wiki.internal.local | 8080 | 8443 |
| API | api.internal.local | 8082 | 8444 |

Ports used by the security tests (not by these services): 8081 (fake HTTP
wiki), 9443 (fake HTTPS wiki), 9444 (unrelated-CA HTTPS test).

### Hosts file

The hostnames must resolve to the machine running the services. Add this line
to `/etc/hosts` (Linux, WSL, Codespaces):

```
127.0.0.1  wiki.internal.local  api.internal.local
```

If you test from a Windows browser, add the same line to
`C:\Windows\System32\drivers\etc\hosts`.

## Generate certificates (once per checkout)

Private keys are never stored in GitHub. Each checkout generates its own Root
CA and matching certificates and keys:

```bash
bash ca/generate-certs.sh
```

Type `REPLACE` when prompted. The script creates:

| File | Purpose |
|---|---|
| `ca/rootCA.crt` / `ca/rootCA.key` | Internal Root CA |
| `ca/wiki/wiki.crt` / `ca/wiki/wiki.key` | Wiki certificate (SAN: `wiki.internal.local`) and key |
| `ca/api/api.crt` / `ca/api/api.key` | API certificate (SAN: `api.internal.local`) and key |
| `tests/certs/fake-wiki.crt` / `.key` | Untrusted self-signed cert for the fake wiki (Member 3) |

Important:

- Every checkout gets a **different** CA. Never copy keys or certificates
  between machines. Generate them locally instead.
- **Never commit `.key` files**, and do not commit the regenerated `.crt`
  files. `git status` will show them as modified. Leave them uncommitted.
- Never use `git add .` or `git add ca/`. Stage specific files only.

Verify the result:

```bash
openssl verify -CAfile ca/rootCA.crt ca/wiki/wiki.crt ca/api/api.crt
```

Both certificates should report `OK`. To confirm each key matches its
certificate, the two hashes in each pair must be identical:

```bash
openssl x509 -noout -pubkey -in ca/wiki/wiki.crt | openssl sha256
openssl pkey -pubout -in ca/wiki/wiki.key | openssl sha256
openssl x509 -noout -pubkey -in ca/api/api.crt | openssl sha256
openssl pkey -pubout -in ca/api/api.key | openssl sha256
```

## Start and stop

Use one terminal per service. Stop a service with `Ctrl+C`, or stop all of
them with `pkill -f services.main`.

| Service | Mode | Command |
|---|---|---|
| Wiki | HTTP | `python -m services.main wiki --mode http` |
| API | HTTP | `python -m services.main api --mode http` |
| Wiki | HTTPS | `python -m services.main wiki --mode https` |
| API | HTTPS | `python -m services.main api --mode https` |

HTTP is the default mode. HTTP and HTTPS instances use different ports, so they
can run at the same time.

In HTTPS mode each service loads only its own certificate and key (see the
table above). If a file is missing, the launcher stops with an error naming it.
Run the certificate generation step first.

By default services bind to `127.0.0.1`. To bind to another interface, set
`BIND_HOST`:

```bash
BIND_HOST=0.0.0.0 python -m services.main wiki --mode http
```

Only expose the services inside the authorized lab environment.

## Expected responses

**Wiki** (`GET /`): an HTML page titled "Internal Organizational Wiki" with a
security notice.

- HTTP mode: "(HTTP Baseline)" and a notice that the page is served over plain
  unencrypted HTTP.
- HTTPS mode: "(HTTPS)" and a notice that the page is served over HTTPS.

**API** (`GET /health`): a small JSON response.

```json
{"status": "healthy", "service": "internal-api", "version": "1.0", "mode": "HTTP"}
```

`mode` is `HTTP` or `HTTPS` depending on how the service was started.

## HTTP baseline

```bash
curl http://wiki.internal.local:8080/
curl http://api.internal.local:8082/health
```

HTTP does not provide TLS encryption or cryptographic server identity
verification. Anyone on the network path can read or modify the traffic, and a
client cannot prove it is talking to the real server. This is the deliberately
vulnerable baseline for the demo.

## HTTPS verification

Use the real hostnames and explicitly trust the project's Root CA. Do **not**
use `curl -k` or `--insecure`, because that disables the verification this
project demonstrates.

```bash
curl --cacert ca/rootCA.crt https://wiki.internal.local:8443/
curl --cacert ca/rootCA.crt https://api.internal.local:8444/health
```

These succeed only when the Root CA is trusted, the server presents the correct
certificate, and the hostname matches the certificate's SAN.

Inspect the TLS handshake for each service:

```bash
openssl s_client -connect wiki.internal.local:8443 -servername wiki.internal.local \
  -CAfile ca/rootCA.crt -verify_hostname wiki.internal.local -verify_return_error </dev/null

openssl s_client -connect api.internal.local:8444 -servername api.internal.local \
  -CAfile ca/rootCA.crt -verify_hostname api.internal.local -verify_return_error </dev/null
```

Look for `Verification: OK` or `Verify return code: 0 (ok)`. If your OpenSSL
version prints differently, the `curl --cacert` commands are the primary
reproducible test.

### Negative test

Without the Root CA, the client has no reason to trust the server, so this
should fail with a certificate verification error:

```bash
curl https://wiki.internal.local:8443/
```

## Attack demo (for Member 3)

1. Generate certificates on the demo machine (`bash ca/generate-certs.sh`).
2. Start the legitimate services in HTTPS mode, one per terminal:

   ```bash
   python -m services.main wiki --mode https
   python -m services.main api --mode https
   ```

3. The legitimate wiki (8443) succeeds with `--cacert ca/rootCA.crt`. The fake
   HTTPS wiki (9443) and the unrelated-CA test (9444) should fail the same
   command, because their certificates were not issued by the Root CA.
4. For the HTTP baseline part of the demo, start the services with
   `--mode http` instead.

## Troubleshooting

| Problem | What to check |
|---|---|
| `ModuleNotFoundError: No module named 'uvicorn'` | Run `pip install fastapi uvicorn`. |
| `ModuleNotFoundError: No module named 'services'` | Run from the repo root with `python -m services.main`, not `python services/main.py`. |
| `Certificate not found` / `Private key not found` | Run `bash ca/generate-certs.sh`. |
| `KEY_VALUES_MISMATCH` | The certificate and key are from different generations, for example after `git pull` replaced the `.crt` files. Run `bash ca/generate-certs.sh` again. |
| `PEM lib` error | A key file is damaged or encrypted. Regenerate with `bash ca/generate-certs.sh`. Do not paste keys through documents. |
| `Could not resolve host` | The hosts-file entry is missing. See "Hosts file". |
| Connection refused | Is the process running? Check the port, interface, and firewall. |
| Hostname mismatch | The URL hostname must match the certificate SAN. Do not disable verification to fix it. |
| Unknown CA | Make sure the client uses `--cacert ca/rootCA.crt` from this checkout. |
| Wrong certificate | Check the cert path for the service and inspect it with `openssl x509 -noout -subject -ext subjectAltName -in <file>`. |

## Security notes

- Private keys (`*.key`, `*.pem`) are blocked by `.gitignore`. Never commit
  them, and never paste them into chat, documents, or slides.
- The Root CA, keys, and fake certificates are for this lab only. Do not reuse
  them for anything real.
- Do not disable certificate verification in any secured test.
- Keep test services inside the authorized lab environment.