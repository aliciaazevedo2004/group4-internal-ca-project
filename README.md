# Group 4 — Internal Certificate Authority

**Course:** ITIS 3200  
**Project:** Internal Certificate Authority Setup for a Small Network

## 1. Project Overview

This project demonstrates how an internal Certificate Authority (CA) can secure communication between clients and internal network services using HTTPS.

Our network includes:

- **Root CA:** Issues and verifies trusted certificates.
- **Internal Wiki:** Web service secured using HTTPS.
- **Internal API:** API service secured using HTTPS.
- **Security Testing:** Demonstrates trusted and untrusted connections.

The goal is to demonstrate how certificate verification protects against server impersonation.

## 2. Project Structure

```text
group4-internal-ca-project/
├── ca/              # Root CA and service certificates
├── services/        # Internal wiki and API
├── tests/           # Security testing scripts
├── docs/            # Test plans, results, and evidence
├── report/          # Final report
├── presentation/    # Presentation slides
└── README.md
```

Private keys are stored locally and are not uploaded to GitHub.

## 3. Requirements

- Python 3.9+
- OpenSSL
- curl
- FastAPI
- Uvicorn
- Ubuntu, WSL, or Linux

Install dependencies:

```bash
python3 -m pip install fastapi uvicorn
```

All commands below are run from the project root.

## 4. Running the Services

The project uses the following ports:

| Service | Port | Protocol |
|---|---|---|
| Internal Wiki | 8080 | HTTP |
| Internal Wiki | 8443 | HTTPS |
| Internal API | 8082 | HTTP |
| Internal API | 8444 | HTTPS |
| Fake HTTP Wiki | 8081 | HTTP |
| Fake HTTPS Wiki | 9443 | HTTPS |

### Start the Legitimate Wiki

```bash
python3 -m services.main wiki --mode https
```

### Start the Internal API

```bash
python3 -m services.main api --mode https
```

Both HTTPS services require their matching certificate and private key files to be available locally.

## 5. Certificate Verification

The Root CA public certificate is stored at:

`ca/rootCA.crt`

Verify the service certificates:

```bash
openssl verify -CAfile ca/rootCA.crt ca/wiki/wiki.crt
openssl verify -CAfile ca/rootCA.crt ca/api/api.crt
```

Expected result: Both certificates verify successfully.

## 6. Security Testing

Three security tests demonstrate the project's main security concepts.

### Test 1 — Fake HTTP Wiki

Demonstrates that HTTP does not provide certificate-based server authentication.

Start the fake server:

```bash
python3 tests/fake_http_wiki.py
```

Test the connection:

```bash
curl -i http://127.0.0.1:8081/
```

**Expected Result:** HTTP connection succeeds without certificate verification.

### Test 2 — Legitimate HTTPS Wiki

Demonstrates that a legitimate HTTPS server is accepted when its certificate is trusted.

Start the legitimate HTTPS wiki:

```bash
python3 -m services.main wiki --mode https
```

Test the connection:

```bash
curl --noproxy '*' \
  --resolve wiki.internal.local:8443:127.0.0.1 \
  --cacert ca/rootCA.crt \
  https://wiki.internal.local:8443/
```

**Expected Result:** HTTPS connection succeeds with certificate and hostname verification.

### Test 3 — Fake HTTPS Wiki

Demonstrates that a fake HTTPS server with an untrusted certificate is rejected.

Start the fake server:

```bash
python3 tests/fake_https_wiki.py
```

Test the connection:

```bash
curl --noproxy '*' \
  --resolve wiki.internal.local:9443:127.0.0.1 \
  --cacert ca/rootCA.crt \
  https://wiki.internal.local:9443/
```

**Expected Result:** Certificate verification fails, typically with curl error `60`.

The fake HTTPS server requires its matching private key, which is stored locally rather than in GitHub.

## 7. Internal API Verification

Verify that the internal API works over HTTPS:

```bash
curl --noproxy '*' \
  --resolve api.internal.local:8444:127.0.0.1 \
  --cacert ca/rootCA.crt \
  https://api.internal.local:8444/health
```

**Expected Result:** The API returns a successful health response over a verified HTTPS connection.

## 8. Documentation

| Location | Description |
|---|---|
| `tests/security-testing-plan.md` | Three security tests and expected outcomes |
| `tests/test-results.md` | Testing results and observations |
| `tests/evidence/` | Terminal output |
| `report/` | Project report |

## 9. Security Considerations

- Private keys are excluded from GitHub.
- The Root CA is used to verify legitimate service certificates.
- Certificate and hostname verification remain enabled.
- Fake services are used only in a controlled testing environment.
- The tests demonstrate server authentication, not mutual TLS (mTLS) client authentication.

## 10. Conclusion

This project demonstrates how an internal Certificate Authority provides trusted identities for internal services.

The three security tests show that HTTP lacks certificate-based authentication, legitimate HTTPS connections can be verified, and fake HTTPS certificates are rejected.

Together, these demonstrations highlight the importance of HTTPS and certificate verification in securing internal network communication.