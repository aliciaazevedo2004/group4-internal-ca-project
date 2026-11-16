# Group 4 — Internal Certificate Authority Setup for a Small Network

**Course:** ITIS 3200  
**Team:** Group 4  
**Project:** Internal Certificate Authority Setup for a Small Network

## 1. Project Overview

This project demonstrates the implementation of an internal Public Key Infrastructure (PKI) for a small office network containing two web services: an internal wiki and an internal API.

A self-signed Root Certificate Authority (CA) establishes the organization's internal trust hierarchy and issues separate X.509 certificates to each service. Transport Layer Security (TLS) protects communication between clients and the legitimate services.

The project includes an HTTP baseline, HTTPS-enabled services, client certificate verification, and controlled attack demonstrations. These components illustrate how certificate-based authentication improves security compared with unencrypted HTTP communication.

### Security Objectives

- **Authentication:** Verify the identities of legitimate internal services.
- **Confidentiality:** Protect data transmitted between clients and services from network eavesdropping.
- **Integrity:** Detect unauthorized modification of transmitted information.
- **Impersonation prevention:** Reject unauthorized services presenting untrusted or incorrectly identified certificates.
- **Certificate management:** Establish a private trust hierarchy using an internal Root CA.
- **Reproducibility:** Provide a consistent environment for service configuration, certificate verification, and security testing.

## 2. Threat Model and Assumptions

The attacker is modeled as an unauthorized host connected to the internal network, potentially through a compromised workstation or rogue device.

### Attacker Capabilities

The attacker may:

- Communicate with internal network services.
- Capture accessible network traffic.
- Host a fake version of the internal wiki.
- Attempt to impersonate legitimate services.
- Generate and present unauthorized TLS certificates.

### Attacker Limitations

The attacker is assumed not to have:

- Access to the legitimate Root CA private key.
- Access to legitimate service private keys.
- Administrative control over legitimate services.
- Permission to modify trusted CA settings on client machines.

The attack demonstrations use isolated endpoints to simulate service impersonation. They do not rely on DNS poisoning, traffic redirection, or interception of real user traffic.

## 3. System Architecture

The environment contains five primary components:

1. **Root Certificate Authority:** Establishes trust and signs service certificates.
2. **Internal Wiki:** Provides an internal website accessible over HTTP and HTTPS.
3. **Internal API:** Provides a health-check endpoint accessible over HTTP and HTTPS.
4. **Trusted Client:** Uses the Root CA certificate to validate HTTPS connections.
5. **Attack Simulation Services:** Provide fake HTTP and HTTPS endpoints for controlled security testing.

### Network Configuration and Port Assignments

| Component | Hostname / Address | Port | Protocol | Purpose |
|---|---|---|---|---|
| Legitimate Wiki | `wiki.internal.local` | 8080 | HTTP | T1 — HTTP baseline |
| Fake Wiki | `wiki.internal.local` | 8081 | HTTP | T2 — HTTP impersonation |
| Legitimate Wiki | `wiki.internal.local` | 8443 | HTTPS | T3 — Trusted HTTPS |
| Fake HTTPS Wiki | `wiki.internal.local` | 9443 | HTTPS | T4 — Self-signed certificate rejection |
| Legitimate Wiki via IP | `127.0.0.1` | 8443 | HTTPS | T5 — Hostname mismatch |
| Unrelated-CA Wiki | `wiki.internal.local` | 9444 | HTTPS | T6 — Unrelated CA rejection |
| Internal API | `api.internal.local` | 8082 | HTTP | API HTTP baseline |
| Internal API | `api.internal.local` | 8444 | HTTPS | API HTTPS verification |

The legitimate services use the ports defined in `services/main.py`. The attack simulation services use separate ports to prevent conflicts with the legitimate services.

All services are intended to run within an authorized local or virtual lab environment.

## 4. Repository Organization

The project organizes legitimate certificates, service implementations, testing scripts, and documentation into separate directories.

```text
group4-internal-ca-project/
├── README.md
├── .gitignore
├── ca/
│   ├── rootCA.crt
│   ├── rootCA.cnf
│   ├── wiki/
│   │   ├── wiki.crt
│   │   ├── wiki.key          # Local only
│   │   ├── wiki.csr
│   │   └── wiki.ext
│   └── api/
│       ├── api.crt
│       ├── api.key           # Local only
│       ├── api.csr
│       └── api.ext
├── services/
│   ├── main.py
│   ├── wiki/
│   └── api/
├── tests/
│   ├── fake_http_wiki.py
│   ├── fake_https_wiki.py
│   ├── security_tests.sh
│   └── certs/
│       ├── t4-self-signed-rejection-ca/
│       │   ├── fake-wiki.crt
│       │   └── fake-wiki.key       # Local only
│       └── t6-unrelated-ca/
│           ├── unrelated-ca.crt
│           ├── unrelated-ca.key   # Local only
│           ├── unrelated-wiki.crt
│           ├── unrelated-wiki.key # Local only
│           └── unrelated-wiki.csr
├── docs/
│   ├── security-testing-plan.md
│   ├── test-results.md
│   ├── attack-demonstration.md
│   ├── integration-checklist.md
│   └── evidence/
├── clients/
├── report/
└── presentation/
```

Private-key files shown in the structure are stored locally and excluded from the public repository.

The project uses two certificate locations:

- `ca/` for the legitimate Root CA and service certificates.
- `tests/certs/` for independent attack-simulation certificates.

No additional certificate directory is required.

## 5. Prerequisites and Environment Setup

### Software Requirements

- Python 3.9 or newer
- OpenSSL
- curl
- Git
- FastAPI
- Uvicorn
- Ubuntu, Windows Subsystem for Linux (WSL), or a compatible Linux environment

### Clone the Repository

```bash
git clone https://github.com/aliciaazevedo2004/group4-internal-ca-project.git
cd group4-internal-ca-project
```

### Install Python Dependencies

```bash
python3 -m pip install fastapi uvicorn
```

### Configure Local Hostname Resolution

The internal hostnames must resolve to the machine hosting the services.

For local testing, add the following line to `/etc/hosts`:

```text
127.0.0.1 wiki.internal.local api.internal.local
```

On Windows, the hosts file is located at:

```text
C:\Windows\System32\drivers\etc\hosts
```

Alternatively, curl can map hostnames directly to local addresses using `--resolve`.

Example:

```bash
curl --noproxy '*' \
  --resolve wiki.internal.local:8080:127.0.0.1 \
  http://wiki.internal.local:8080/
```

All commands are executed from the repository root unless otherwise specified.

## 6. Root CA and Service Certificate Generation

The project uses OpenSSL to create a self-signed Root CA and issue separate service certificates.

### Certificate Files

| File | Description |
|---|---|
| `ca/rootCA.crt` | Public Root CA certificate |
| `ca/rootCA.cnf` | Root CA configuration |
| `ca/wiki/wiki.crt` | Wiki service certificate |
| `ca/wiki/wiki.csr` | Wiki certificate signing request |
| `ca/wiki/wiki.ext` | Wiki certificate extensions |
| `ca/api/api.crt` | API service certificate |
| `ca/api/api.csr` | API certificate signing request |
| `ca/api/api.ext` | API certificate extensions |

The wiki certificate identifies `wiki.internal.local`, and the API certificate identifies `api.internal.local` through their Subject Alternative Name extensions.

### Certificate Generation Procedure

To generate a complete certificate setup, create a Root CA and sign each service certificate using that CA.

The following commands create a new certificate hierarchy. They should be used in a separate working copy or with new output filenames if the existing certificate setup must be preserved.

**Generate the Root CA private key:**

```bash
openssl genrsa -out ca/rootCA.key 3072
```

**Generate the self-signed Root CA certificate:**

```bash
openssl req -x509 -new -sha256 \
  -key ca/rootCA.key \
  -days 365 \
  -out ca/rootCA.crt \
  -subj "/C=US/ST=North-Carolina/L=Charlotte/CN=Group 4 Internal Root CA" \
  -addext "basicConstraints=critical,CA:TRUE" \
  -addext "keyUsage=critical,keyCertSign,cRLSign"
```

**Generate the wiki private key and certificate signing request:**

```bash
openssl genrsa -out ca/wiki/wiki.key 2048

openssl req -new \
  -key ca/wiki/wiki.key \
  -out ca/wiki/wiki.csr \
  -subj "/C=US/ST=North-Carolina/L=Charlotte/CN=wiki.internal.local"
```

**Sign the wiki certificate:**

```bash
openssl x509 -req \
  -in ca/wiki/wiki.csr \
  -CA ca/rootCA.crt \
  -CAkey ca/rootCA.key \
  -CAcreateserial \
  -out ca/wiki/wiki.crt \
  -days 365 \
  -sha256 \
  -extfile ca/wiki/wiki.ext \
  -extensions server_cert
```

**Generate the API private key and certificate signing request:**

```bash
openssl genrsa -out ca/api/api.key 2048

openssl req -new \
  -key ca/api/api.key \
  -out ca/api/api.csr \
  -subj "/C=US/ST=North-Carolina/L=Charlotte/CN=api.internal.local"
```

**Sign the API certificate:**

```bash
openssl x509 -req \
  -in ca/api/api.csr \
  -CA ca/rootCA.crt \
  -CAkey ca/rootCA.key \
  -CAcreateserial \
  -out ca/api/api.crt \
  -days 365 \
  -sha256 \
  -extfile ca/api/api.ext \
  -extensions server_cert
```

The generated certificate and private-key pairs remain in their respective `ca/` subdirectories.

### Verify the Certificates

```bash
openssl verify -CAfile ca/rootCA.crt ca/wiki/wiki.crt
openssl verify -CAfile ca/rootCA.crt ca/api/api.crt
```

The expected verification output is:

```text
ca/wiki/wiki.crt: OK
ca/api/api.crt: OK
```

These commands verify the certificate chains; successful HTTPS operation also requires the matching private keys and correct server configuration.

## 7. Starting the HTTP Services

The HTTP baseline demonstrates communication without TLS encryption or certificate-based server authentication.

Start each service in a separate terminal.

### Internal Wiki — Port 8080

```bash
python3 -m services.main wiki --mode http
```

Verify:

```bash
curl -i http://127.0.0.1:8080/
```

Expected response: HTTP `200 OK` with the internal wiki page.

### Internal API — Port 8082

```bash
python3 -m services.main api --mode http
```

Verify:

```bash
curl -i http://127.0.0.1:8082/health
```

Expected response: HTTP `200 OK` with a JSON health response.

Stop a service with `Ctrl+C`.

## 8. Starting the HTTPS Services

The HTTPS services use the legitimate certificates and matching private keys stored under `ca/`.

### Certificate Paths

| Service | Certificate | Private Key | HTTPS Port |
|---|---|---|---|
| Wiki | `ca/wiki/wiki.crt` | `ca/wiki/wiki.key` | 8443 |
| API | `ca/api/api.crt` | `ca/api/api.key` | 8444 |

### Start the Wiki

```bash
python3 -m services.main wiki --mode https
```

### Start the API

```bash
python3 -m services.main api --mode https
```

### Verify the Wiki

```bash
curl -v --noproxy '*' \
  --resolve wiki.internal.local:8443:127.0.0.1 \
  --cacert ca/rootCA.crt \
  https://wiki.internal.local:8443/
```

### Verify the API

```bash
curl -v --noproxy '*' \
  --resolve api.internal.local:8444:127.0.0.1 \
  --cacert ca/rootCA.crt \
  https://api.internal.local:8444/health
```

A successful connection confirms that the client can communicate with the service while verifying its certificate chain and hostname.

## 9. Client Trust and Certificate Verification

The client uses the internal Root CA certificate as its trust anchor.

```text
ca/rootCA.crt
```

Certificate verification includes:

- Validating the certificate chain.
- Confirming the server certificate was issued by a trusted CA.
- Checking the certificate's validity period.
- Verifying the requested hostname against the certificate's SAN.
- Confirming the certificate is suitable for server authentication.

### OpenSSL Verification

```bash
openssl s_client \
  -connect wiki.internal.local:8443 \
  -servername wiki.internal.local \
  -CAfile ca/rootCA.crt \
  -verify_hostname wiki.internal.local \
  -verify_return_error
```

A correctly configured legitimate service should produce a successful verification result.

Certificate verification must remain enabled. The `curl -k` and `--insecure` options are not used because they bypass certificate validation.

## 10. Security Testing and Attack Demonstrations

The project includes six controlled security tests.

### Test Matrix

| Test | Scenario | Expected Outcome |
|---|---|---|
| T1 | Legitimate HTTP wiki | HTTP connection accepted |
| T2 | Fake HTTP wiki | Fake HTTP connection accepted |
| T3 | Legitimate HTTPS wiki | Trusted certificate accepted |
| T4 | Self-signed fake HTTPS wiki | Certificate rejected |
| T5 | Hostname/IP mismatch | Certificate rejected |
| T6 | Unrelated CA certificate | Certificate rejected |

### T1 — Legitimate HTTP Wiki

Start the legitimate HTTP wiki:

```bash
python3 -m services.main wiki --mode http
```

Run:

```bash
curl -i http://wiki.internal.local:8080/
```

**Expected outcome:** HTTP `200 OK`.

This establishes the legitimate HTTP baseline.

### T2 — Fake HTTP Wiki

Start the fake HTTP wiki:

```bash
python3 tests/fake_http_wiki.py
```

Run:

```bash
curl -i http://wiki.internal.local:8081/
```

**Expected outcome:** HTTP `200 OK` from the fake wiki.

The test demonstrates that HTTP does not cryptographically authenticate the server.

### T3 — Legitimate HTTPS Wiki

Start the legitimate HTTPS wiki:

```bash
python3 -m services.main wiki --mode https
```

Run:

```bash
curl -v --noproxy '*' \
  --resolve wiki.internal.local:8443:127.0.0.1 \
  --cacert ca/rootCA.crt \
  https://wiki.internal.local:8443/
```

**Expected outcome:** Certificate verification succeeds and the legitimate wiki responds.

### T4 — Self-Signed Fake HTTPS Wiki

The self-signed fake HTTPS wiki uses the independent test certificate stored under:

```text
tests/certs/t4-self-signed-rejection-ca/
```

Start the fake HTTPS server:

```bash
python3 tests/fake_https_wiki.py
```

Run:

```bash
curl -v --noproxy '*' \
  --resolve wiki.internal.local:9443:127.0.0.1 \
  --cacert ca/rootCA.crt \
  https://wiki.internal.local:9443/
```

**Expected outcome:** Certificate verification fails, typically with curl exit code `60`.

This demonstrates that a matching hostname does not establish trust when the certificate is not issued by a trusted CA.

### T5 — Hostname/IP Mismatch

The hostname mismatch test connects to the legitimate HTTPS wiki using an IP address not covered by its certificate SAN.

Run:

```bash
curl -v --noproxy '*' \
  --cacert ca/rootCA.crt \
  https://127.0.0.1:8443/
```

**Expected outcome:** Hostname/IP verification fails, typically with curl exit code `60`.

The legitimate wiki certificate identifies `wiki.internal.local`, not `127.0.0.1`.

### T6 — Unrelated Certificate Authority

The unrelated-CA test uses a fake wiki certificate issued by an independent CA.

The public certificates are stored in:

```text
tests/certs/t6-unrelated-ca/
```

Start an HTTPS test server on port `9444` using the unrelated wiki certificate and its matching private key.

Run:

```bash
curl -v --noproxy '*' \
  --resolve wiki.internal.local:9444:127.0.0.1 \
  --cacert ca/rootCA.crt \
  https://wiki.internal.local:9444/
```

**Expected outcome:** Certificate verification fails, typically with curl exit code `60`.

This demonstrates that certificates issued by unrelated CAs are not automatically trusted by clients configured to trust the internal Root CA.

### Interpreting Test Results

For T1–T3, a successful result requires an HTTP response from the intended service. T3 additionally requires successful TLS verification.

For T4–T6, the intended successful security outcome is certificate rejection.

A connection refusal, missing server, DNS error, or TLS startup failure does not count as successful certificate rejection.

## 11. Test Results and Evidence

The security tests evaluate the following outcomes:

| Test | Expected Security Result |
|---|---|
| T1 | Legitimate HTTP service responds |
| T2 | Fake HTTP service responds without TLS authentication |
| T3 | Trusted HTTPS certificate and hostname are accepted |
| T4 | Self-signed fake HTTPS certificate is rejected |
| T5 | Incorrect hostname/IP is rejected |
| T6 | Unrelated-CA certificate is rejected |

Detailed execution records and supporting evidence are maintained separately from this README.

Each test record includes:

- Test identifier and execution date.
- Command and target URL.
- Expected and actual results.
- curl exit status.
- PASS/FAIL determination.
- Relevant terminal output or screenshots.
- Interpretation of the security principle demonstrated.

Supporting documentation:

- `docs/security-testing-plan.md`
- `docs/test-results.md`
- `docs/evidence/`

The README describes the complete test procedure; the test-results document is the authoritative record of observed execution outcomes.

## 12. Automated Security Testing

The repository includes `tests/security_tests.sh` as the location for automated security checks.

The automated testing procedure evaluates the six test scenarios and distinguishes successful connections from expected certificate-validation failures.

For negative tests, certificate rejection must be caused by the intended trust or hostname validation error rather than an unrelated connection problem.

The manual commands in Section 10 can also be used to reproduce and inspect each test individually.

## 13. Independent Attack Certificate Configuration

The attack demonstrations use certificates separate from the legitimate Root CA.

### T4 — Self-Signed Certificate

The self-signed fake wiki certificate is stored at:

```text
tests/certs/t4-self-signed-rejection-ca/fake-wiki.crt
```

Its matching private key is stored locally at:

```text
tests/certs/t4-self-signed-rejection-ca/fake-wiki.key
```

### T6 — Unrelated CA

The unrelated-CA test uses:

```text
tests/certs/t6-unrelated-ca/unrelated-ca.crt
tests/certs/t6-unrelated-ca/unrelated-wiki.crt
```

The corresponding private keys are maintained locally.

### Reproducing the Attack Certificates

To reproduce the attack certificate setup:

1. Generate a self-signed certificate and matching private key for the T4 fake wiki.
2. Generate a separate Root CA for the T6 simulation.
3. Generate a private key and CSR for the unrelated fake wiki.
4. Sign the fake wiki certificate using the unrelated CA.
5. Configure the fake HTTPS servers with their corresponding certificate/key pairs.
6. Run the verification tests with the legitimate Root CA as the trust anchor.

The attack certificates must remain separate from the legitimate CA hierarchy.

Private keys must not be committed to GitHub.

## 14. Known Limitations and Mutual TLS

The primary focus of this project is TLS server authentication using an internal Root CA.

### Mutual TLS (mTLS)

Mutual TLS requires both clients and servers to authenticate using certificates.

The demonstrated architecture focuses on server authentication, where the client verifies the identity of the wiki or API.

Client-certificate authentication is outside the demonstrated server-authentication test scope.

### Other Limitations

- The environment uses local or virtual network interfaces for controlled testing.
- The impersonation simulations do not perform DNS poisoning or transparent traffic interception.
- The tests focus on certificate trust and hostname verification rather than every possible PKI attack.
- The public repository intentionally excludes private keys.
- Reproduction requires locally available matching certificate/private-key pairs.

## 15. Private-Key Handling and Repository Security

The repository excludes private keys and sensitive configuration files through `.gitignore`.

```gitignore
*.key
*.pem
*.p12
.env
```

Security practices include:

- Keeping the Root CA private key separate from service hosts.
- Restricting access to private-key files.
- Excluding service private keys from the public repository.
- Excluding attack-simulation private keys from the public repository.
- Using matching certificate/private-key pairs.
- Keeping legitimate and attack certificates in separate directories.
- Maintaining certificate verification during HTTPS testing.
- Avoiding sensitive information in screenshots and test evidence.

Public certificates, certificate signing requests, configuration files, scripts, and non-sensitive evidence may be committed.

## 16. Project Documentation

| File or Directory | Description |
|---|---|
| `ca/` | Root CA and legitimate service certificates |
| `services/README.md` | Wiki and API configuration |
| `clients/README.md` | Client trust configuration |
| `docs/security-testing-plan.md` | Security-testing methodology |
| `docs/test-results.md` | Actual test results and observations |
| `docs/attack-demonstration.md` | Attack demonstration documentation |
| `docs/integration-checklist.md` | Integration verification checklist |
| `docs/evidence/` | Terminal output and screenshots |
| `tests/certs/` | Independent attack certificates |
| `report/` | Project report materials |
| `presentation/` | Presentation materials |

## 17. Project Verification Checklist

The project verification process covers:

- [ ] Root CA certificate and configuration verified.
- [ ] Wiki and API certificate chains verified.
- [ ] Service certificates contain the correct SANs.
- [ ] Private keys are excluded from GitHub.
- [ ] Legitimate HTTP wiki and API respond successfully.
- [ ] Legitimate HTTPS wiki and API respond with valid certificates.
- [ ] Client trust configuration verifies the internal Root CA.
- [ ] T1–T6 produce their expected security outcomes.
- [ ] Test results and evidence are documented.
- [ ] Certificate-generation instructions are reproducible.
- [ ] Final documentation is consistent with the implementation.

This checklist is intended for final verification rather than a record of completed tests.

## 18. Conclusion

The Internal Certificate Authority project demonstrates how an organization can establish trusted service identities within a private network.

The HTTP baseline illustrates the absence of TLS-based server authentication, while the HTTPS configuration provides certificate-based identity verification, confidentiality, and integrity protection.

The attack demonstrations illustrate the importance of validating certificate chains and hostnames. By distinguishing legitimate services from self-signed, incorrectly identified, and unrelated-CA services, the project demonstrates fundamental PKI security principles.

The project provides a practical foundation for understanding internal certificate authorities, TLS configuration, secure private-key handling, and certificate-based service authentication.
