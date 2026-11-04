# Security Testing Plan

## 1. Objective
Verify that the internal Certificate Authority (CA) protects the internal wiki and API against unencrypted communication and server impersonation.

## 2. Lab Topology & Port Allocations
All tests execute locally using loopback resolution mapped to the simulated internal domain `wiki.internal.local`.

- **DNS / Host Mapping (`/etc/hosts`):** `127.0.0.1 wiki.internal.local`
- **Legitimate HTTP Wiki:** `http://wiki.internal.local:8080/`
- **Fake HTTP Wiki:** `http://wiki.internal.local:8081/`
- **Legitimate HTTPS Wiki:** `https://wiki.internal.local:8443/` (Secured via `ca/rootCA.crt`)
- **Fake HTTPS Wiki:** `https://wiki.internal.local:9443/` (Untrusted / Self-signed certificate)

---

## 3. Test Matrix

| Test ID | Scenario | Command / Target | Expected Result | What It Demonstrates |
| :--- | :--- | :--- | :--- | :--- |
| **T1** | HTTP client connects to legitimate wiki. | `curl -i http://wiki.internal.local:8080/` | HTTP 200 OK | Baseline service is reachable without TLS authentication. |
| **T2** | HTTP client connects to fake wiki. | `curl -i http://wiki.internal.local:8081/` | HTTP 200 OK | HTTP itself does not authenticate the server identity. |
| **T3** | Verified TLS client connects to legitimate wiki using `rootCA.crt`. | `curl -v --cacert ca/rootCA.crt https://wiki.internal.local:8443/` | Success (TLS handshake succeeds, HTTP 200) | Trusted chain and correct hostname are accepted. |
| **T4** | Verified TLS client connects to fake server with an untrusted certificate. | `curl -v --cacert ca/rootCA.crt https://wiki.internal.local:9443/` | Handshake Failure (`SSL certificate problem: self signed certificate` / exit code 60) | Client rejects a certificate it cannot validate to its configured trust anchor. |
| **T5** | Verified TLS client connects to a server certificate signed by internal CA but with wrong SAN. | `curl -v --cacert ca/rootCA.crt https://127.0.0.1:8443/` | Handshake Failure (Hostname mismatch) | Trust in a CA does not remove hostname verification. |
| **T6** | Verified TLS client connects to a certificate signed by an unrelated CA. | `curl -v --cacert ca/rootCA.crt https://unrelated.internal.local:8443/` | Handshake Failure (Unknown issuer) | Client trusts the configured CA, not arbitrary issuers. |

---

## 4. Evidence Collection Standards
For each executed test case, we recorded the following in `docs/test-results.md`:
- Test ID and timestamp of execution
- Complete command line invocation
- Expected result vs. actual result
- PASS / FAIL status
- Verbatim terminal output / handshake transcript
