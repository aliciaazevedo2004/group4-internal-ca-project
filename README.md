# Group 4 — Internal Certificate Authority

**Course:** ITIS 3200  
**Project:** Internal Certificate Authority Setup for a Small Network

## Project Overview

This project demonstrates how an internal Certificate Authority (CA) secures an internal wiki and API using HTTPS.

The project includes a Root CA, service certificates, two internal services, and three security tests.

## Project Structure

```text
group4-internal-ca-project/
├── ca/          # Root CA and certificates
├── services/    # Internal wiki and API
├── tests/       # Security tests, certs, and evidence
├── report/      # Report and integration checklist
└── README.md
```

Private keys are stored locally and excluded from GitHub.

## Requirements

- Python 3.9+
- OpenSSL
- curl
- FastAPI and Uvicorn

Install dependencies:

```bash
python3 -m pip install fastapi uvicorn
```

Run all commands from the project root.

## Services

| Service | HTTP | HTTPS |
|---|---|---|
| Internal Wiki | 8080 | 8443 |
| Internal API | 8082 | 8444 |
| Fake HTTP Wiki | 8081 | — |
| Fake HTTPS Wiki | — | 9443 |

Start the legitimate HTTPS services in separate terminals:

```bash
python3 -m services.main wiki --mode https
python3 -m services.main api --mode https
```

Both services require their matching private keys locally.

## Certificate Verification

Verify the wiki and API certificates:

```bash
openssl verify -CAfile ca/rootCA.crt ca/wiki/wiki.crt
openssl verify -CAfile ca/rootCA.crt ca/api/api.crt
```

**Expected:** Both certificates verify successfully.

## Security Testing

| Test | Purpose | Expected Result |
|---|---|---|
| Test 1 — Fake HTTP Wiki | Demonstrate lack of server authentication | HTTP 200 OK |
| Test 2 — Legitimate HTTPS Wiki | Verify trusted certificate | Connection succeeds |
| Test 3 — Fake HTTPS Wiki | Reject untrusted certificate | Curl error 60 |

Start these servers in separate terminals:

```bash
python3 tests/fake_http_wiki.py
python3 -m services.main wiki --mode https
python3 tests/fake_https_wiki.py
```

Run the automated tests:

```bash
bash tests/security_tests.sh
```

The script displays PASS/FAIL results and saves logs in `tests/evidence/` once its log path is updated.

## Internal API Verification

Verify the API over HTTPS:

```bash
curl --noproxy '*' \
  --resolve api.internal.local:8444:127.0.0.1 \
  --cacert ca/rootCA.crt \
  https://api.internal.local:8444/health
```

**Expected:** Successful HTTPS connection and JSON health response.

## Documentation

- `services/README.md` — Service setup
- `tests/security-testing-plan.md` — Testing plan
- `tests/test-results.md` — Test results
- `tests/evidence/` — Testing evidence
- `report/integration-checklist.md` — Project progress

## Security Notes

- Private keys are not committed to GitHub.
- Certificates use the internal Root CA.
- Certificate and hostname verification remain enabled.
- Fake servers are used only for authorized local testing.

## Conclusion

This project demonstrates how HTTPS and an internal Certificate Authority protect internal services from server impersonation through certificate verification.
