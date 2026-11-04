# Security Testing Plan

## Objective
Verify that the internal Certificate Authority (CA) protects the group's internal wiki and API against unencrypted communication and server impersonation.

## Lab Topology & Service Configuration
All tests run against loopback addresses mapped to the agreed simulated domain `wiki.internal.local`.

- **Local DNS Mapping (`/etc/hosts`):** `127.0.0.1 wiki.internal.local`
- **Legitimate HTTP Wiki:** `http://wiki.internal.local:8080/`
- **Fake HTTP Wiki:** `http://wiki.internal.local:8081/`
- **Legitimate HTTPS Wiki:** `https://wiki.internal.local:8443/` (Validated by `ca/rootCA.crt`)
- **Fake HTTPS Wiki:** `https://wiki.internal.local:9443/` (Untrusted / Self-signed certificate)

---

## Test Cases

| ID | Test Scenario | Command / Target | Expected Result | What It Demonstrates |
|---|---|---|---|---|
| **T1** | Connect to HTTP baseline | `curl -i http://wiki.internal.local:8080/` | HTTP 200 OK | Baseline service is reachable without TLS authentication. |
| **T2** | Connect to fake HTTP service in isolated lab | `curl -i http://wiki.internal.local:8081/` | HTTP 200 OK | Plain HTTP cannot authenticate server identity or distinguish impostors. |
| **T3** | Connect to legitimate HTTPS using team root CA | `curl --cacert ca/rootCA.crt https://wiki.internal.local:8443/` | HTTP 200 OK (Handshake success) | Trusted chain and valid hostname are accepted. |
| **T4** | Connect to HTTPS using untrusted certificate | `curl --cacert ca/rootCA.crt https://wiki.internal.local:9443/` | Handshake failure (SSL error 60 / untrusted cert) | Client rejects certificates that do not chain to its trust anchor. |
| **T5** | Connect using hostname not matching certificate SAN | `curl --cacert ca/rootCA.crt https://127.0.0.1:8443/` | Handshake failure (Hostname mismatch error) | Trust in a CA does not bypass hostname validation. |
| **T6** | Connect to certificate signed by unrelated CA | `curl --cacert ca/rootCA.crt https://<UNRELATED_CA_SERVER>/` | Handshake failure (Unknown issuer) | Client trusts only the configured CA, not arbitrary issuers. |

---

## Evidence Collection
For each test, record in `docs/test-results.md`:
- Test ID and timestamp
- Setup and exact command executed
- Expected result vs. actual result
- Pass/Fail status
- Raw terminal transcript / verbose curl output

## Security Notes
Certificate verification must remain enabled across all tests. Never use `--insecure` or `-k` flags during validation tests. All testing is conducted exclusively within the authorized local lab environment.
