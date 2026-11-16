# Internal Services (Wiki and API)

This project uses two FastAPI services: an internal wiki and an internal API. Both support HTTP and HTTPS to demonstrate secure communication using an internal Certificate Authority (CA).

## Setup

Requires Python 3.9+.

Install dependencies:

```bash
python3 -m pip install fastapi uvicorn
```

Run all commands from the repository root.

## Hostnames and Ports

| Service | Hostname | HTTP | HTTPS |
|---|---|---|---|
| Wiki | `wiki.internal.local` | 8080 | 8443 |
| API | `api.internal.local` | 8082 | 8444 |

Security testing uses two additional ports:

- **8081:** Fake HTTP wiki
- **9443:** Fake HTTPS wiki

For local testing, use curl's `--resolve` option or add the following line to your hosts file:

```text
127.0.0.1 wiki.internal.local api.internal.local
```

## Starting the Services

Run each service in a separate terminal.

| Service | Command |
|---|---|
| Wiki HTTP | `python3 -m services.main wiki --mode http` |
| Wiki HTTPS | `python3 -m services.main wiki --mode https` |
| API HTTP | `python3 -m services.main api --mode http` |
| API HTTPS | `python3 -m services.main api --mode https` |

Stop a service with `Ctrl+C`.

By default, services run on `127.0.0.1`.

## HTTP Verification

Verify the HTTP wiki:

```bash
curl http://127.0.0.1:8080/
```

Verify the HTTP API:

```bash
curl http://127.0.0.1:8082/health
```

Both should return successful responses.

HTTP does not provide TLS encryption or certificate-based server authentication.

## HTTPS Configuration

Each service uses a certificate signed by the internal Root CA.

| Service | Certificate | Private Key |
|---|---|---|
| Wiki | `ca/wiki/wiki.crt` | `ca/wiki/wiki.key` |
| API | `ca/api/api.crt` | `ca/api/api.key` |

The Root CA certificate is located at `ca/rootCA.crt`.

Private keys are stored locally and excluded from GitHub.

## HTTPS Verification

Start the wiki and API in HTTPS mode.

**Verify the wiki:**

```bash
curl --noproxy '*' \
  --resolve wiki.internal.local:8443:127.0.0.1 \
  --cacert ca/rootCA.crt \
  https://wiki.internal.local:8443/
```

**Verify the API:**

```bash
curl --noproxy '*' \
  --resolve api.internal.local:8444:127.0.0.1 \
  --cacert ca/rootCA.crt \
  https://api.internal.local:8444/health
```

Expected result: Both HTTPS connections succeed when the certificate chain and hostname are valid.

Do not use `curl -k` or `--insecure`, because these options disable certificate verification.

## Security Demonstration

The project uses three security tests:

| Test | Description | Expected Result |
|---|---|---|
| Test 1 | Fake HTTP Wiki | Connection accepted without certificate verification |
| Test 2 | Legitimate HTTPS Wiki | Trusted certificate accepted |
| Test 3 | Fake HTTPS Wiki | Untrusted certificate rejected |

The internal API is verified separately over HTTPS.

### Run Automated Tests

Start the legitimate HTTPS wiki, fake HTTP wiki, and fake HTTPS wiki in separate terminals.

Then run:

```bash
bash tests/security_tests.sh
```

The script displays PASS/FAIL results and saves a log in `docs/evidence/`.

## Security Notes

- The Root CA signs the legitimate service certificates.
- Each certificate identifies its service hostname through a Subject Alternative Name (SAN).
- HTTPS provides encryption and server authentication.
- Untrusted certificates are rejected when verification is enabled.
- Private keys must never be committed to GitHub.
- Testing is performed in an authorized local environment.

## Conclusion

The wiki and API demonstrate how internal services can use HTTPS with certificates issued by a trusted internal CA.

The three security tests demonstrate the difference between unsecured HTTP, trusted HTTPS, and untrusted HTTPS connections.
