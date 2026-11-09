# Security Testing Plan

**Project:** Internal Certificate Authority Setup for a Small Network — Group 4  
**Role:** Member 3 — Attack Demonstration and Security Testing  
**Environment:** Ubuntu on Windows Subsystem for Linux (WSL)  
**Document status:** October 28 planning deliverable — proposed independent-lab configuration; team-wide endpoint assignments pending confirmation

## 1. Objective

Demonstrate that plain HTTP does not provide certificate-based server authentication and that a client configured to trust the internal Root Certificate Authority (CA) accepts the legitimate HTTPS wiki while rejecting impersonating servers with invalid certificates.

The overall project also includes an internal API. The six security test cases below focus on wiki impersonation and certificate validation; verification of the API is part of the broader team integration effort.

## 2. Lab Topology and Port Allocations

The independent lab will run on Ubuntu through WSL, using the loopback interface to keep the demonstration isolated. The proposed hostname is `wiki.internal.local`, mapped locally through `/etc/hosts`:

```text
127.0.0.1 wiki.internal.local
```

| Endpoint | Proposed URL | Purpose |
| --- | --- | --- |
| Legitimate HTTP wiki | `http://wiki.internal.local:8080/` | HTTP baseline |
| Fake HTTP wiki | `http://wiki.internal.local:8081/` | Controlled HTTP impersonation simulation |
| Legitimate HTTPS wiki | `https://wiki.internal.local:8443/` | Trusted certificate and hostname verification |
| Fake HTTPS wiki | `https://wiki.internal.local:9443/` | Untrusted/self-signed certificate |
| Unrelated-CA HTTPS test service | `https://wiki.internal.local:9444/` | Certificate issued by a different, untrusted CA |

The wrong-hostname test reuses port 8443 under the assumptions specified below. All addresses and ports are proposed for this controlled lab, not assertions about currently running services.

Using the same hostname with different ports simulates access to a fake service. It does **not** demonstrate traffic interception, DNS poisoning, or automatic redirection from the legitimate service to the fake service.

## 3. Test Matrix

| Test ID | Scenario | Planned command | Expected result | What it demonstrates |
| --- | --- | --- | --- | --- |
| **T1** | Client connects to legitimate HTTP wiki | `curl -i http://wiki.internal.local:8080/` | HTTP response received (ideally `200 OK`) | HTTP service is reachable without TLS server authentication. |
| **T2** | Client connects to fake HTTP wiki | `curl -i http://wiki.internal.local:8081/` | HTTP response received (ideally `200 OK`) | HTTP alone does not cryptographically authenticate the server. |
| **T3** | Client verifies legitimate HTTPS wiki with internal CA | `curl -v --cacert ca/rootCA.crt https://wiki.internal.local:8443/` | Verified HTTPS connection succeeds; expected HTTP response | A trusted certificate chain and matching hostname are accepted. |
| **T4** | Client connects to fake HTTPS wiki presenting an untrusted certificate | `curl -v --cacert ca/rootCA.crt https://wiki.internal.local:9443/` | Certificate verification fails; typically curl exit code `60` | Client rejects a certificate that does not chain to the configured trusted CA. |
| **T5** | Client requests a hostname/IP not covered by the legitimate certificate SAN | `curl -v --cacert ca/rootCA.crt https://127.0.0.1:8443/` | Hostname/IP verification fails; typically curl exit code `60` | A trusted CA signature does not override hostname verification. |
| **T6** | Client connects to service presenting a certificate from an unrelated CA | `curl -v --cacert ca/rootCA.crt https://wiki.internal.local:9444/` | Certificate verification fails; typically curl exit code `60` | Trusting the internal CA does not imply trusting unrelated issuers. |

### Test prerequisites and interpretation

- `ca/rootCA.crt` is a **proposed relative path**. It must point to the internal Root CA's public certificate when tests are executed; it is not a claim that the file already exists.
- T1 and T2 require two running HTTP endpoints. A successful response from both demonstrates the absence of *TLS-based* server authentication, not proof that an attacker can transparently replace a legitimate server.
- T3 requires a running HTTPS wiki with a valid certificate signed by the internal CA and a SAN matching `wiki.internal.local`.
- T4 requires the fake HTTPS endpoint to present a certificate not trusted by the internal CA. Do not use the internal Root CA private key to create this fake certificate.
- T5 assumes the legitimate wiki certificate contains `wiki.internal.local` as a DNS SAN **but does not contain `127.0.0.1` as an IP SAN**, and that the service is reachable through `127.0.0.1:8443`. If these assumptions do not hold, use a dedicated wrong-SAN certificate/endpoint instead.
- T6 requires a **separate HTTPS endpoint** on port 9444 that presents a certificate issued by an unrelated CA. Changing only the URL hostname is insufficient to test an unrelated issuer.
- HTTPS verification must remain enabled. Do not use `curl -k` or `--insecure` for T3–T6. Exact error messages can vary by curl/OpenSSL version; the expected result is certificate/hostname validation rejection, not a particular error string.
- In the automated test script, a negative test (T4–T6) should count as **PASS only when it fails for the intended certificate-validation reason**, not for unrelated issues such as connection refusal or DNS resolution failure. For positive tests (T1–T3), the script should confirm an actual HTTP response; for T3, it must not bypass TLS verification.
- `curl --cacert` identifies the intended trust anchor, but the client trust configuration and any environment-specific trust settings must be reviewed during implementation. Test results should include evidence of the certificate verification outcome.

## 4. Evidence Collection Standards

After executing each test, record the following in `docs/test-results.md`:

- Test ID and timestamp
- Full command and target URL
- Expected result and actual result
- PASS/FAIL status
- Relevant terminal output, curl exit status, and certificate verification details
- Short explanation of why the result demonstrates the security principle

## 5. Threat Model and Scope

The simulated attacker controls an unauthorized host that can communicate with internal services and host a fake wiki. The attacker is assumed **not** to possess the internal Root CA private key, alter client trust settings, or administer the legitimate services.

Tests must remain within authorized lab systems, containers, or loopback interfaces. The fake service will be clearly labeled as a lab simulation in its implementation.
