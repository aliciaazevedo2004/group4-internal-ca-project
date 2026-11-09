# Security Test Results

**Project:** Group 4 — Internal Certificate Authority Setup for a Small Network  
**Responsible role:** Member 3 — Attack Demonstration and Security Testing  
**Test environment:** Ubuntu via Windows Subsystem for Linux (WSL)  
**Document status:** Test execution pending  
**Last updated:** November 8, 2026

## 1. Purpose

This document will record observed results and supporting evidence for the security tests defined in the team's security testing plan. The tests compare an HTTP baseline with HTTPS connections that validate the server's certificate chain and hostname. Expected results are stated in advance; actual results will be entered only after execution.

## 2. Proposed Lab Configuration

The following values are proposed for Member 3's isolated, loopback-only test environment and are **not yet confirmed as the team's final service configuration**.

| Component | Address | Purpose |
| --- | --- | --- |
| Legitimate HTTP wiki | `http://wiki.internal.local:8080/` | HTTP baseline |
| Fake HTTP wiki | `http://wiki.internal.local:8081/` | Controlled impersonation simulation |
| Legitimate HTTPS wiki | `https://wiki.internal.local:8443/` | Trusted server certificate |
| Fake HTTPS wiki | `https://wiki.internal.local:9443/` | Untrusted certificate |
| Unrelated-CA HTTPS endpoint | `https://wiki.internal.local:9444/` | Certificate issued by another CA |

**Proposed local hostname mapping:** `127.0.0.1 wiki.internal.local` in `/etc/hosts`.

**Planned tools:** `curl`, OpenSSL, and local test services. The `ca/rootCA.crt` path in the commands below is provisional and must be checked against the repository layout before execution. Tests are limited to authorized project systems. Private keys and passphrases must not appear in evidence or be committed to the public repository.

The separate legitimate API is part of the overall project, but the six mandatory Member 3 test cases below focus on the wiki. API validation can be documented separately during integration.

## 3. Test Summary

| ID | Scenario | Expected result | Actual result | Status |
| --- | --- | --- | --- | --- |
| T1 | Legitimate wiki over HTTP | HTTP response received | Pending | Not Run |
| T2 | Fake wiki over HTTP | HTTP response received | Pending | Not Run |
| T3 | Legitimate wiki over verified HTTPS | Trusted certificate and hostname accepted | Pending | Not Run |
| T4 | Fake HTTPS server with untrusted certificate | Certificate validation rejects connection | Pending | Not Run |
| T5 | Trusted-CA certificate with incorrect hostname | Hostname verification rejects connection | Pending | Not Run |
| T6 | Certificate issued by unrelated CA | Certificate chain verification rejects connection | Pending | Not Run |

A test is **PASS** only if the observed behavior matches its expected result, including successful verified TLS for T3 and rejection by certificate validation for T4–T6. Connection failures caused by a stopped server, wrong port, or DNS issue do **not** count as successful certificate-rejection tests.

## 4. Individual Test Records

### T1 — Legitimate HTTP Wiki

**Objective:** Establish that the legitimate wiki responds over HTTP without TLS-based server authentication.

**Planned command:**

```bash
curl -i http://wiki.internal.local:8080/
```

**Expected result:** The legitimate wiki returns an HTTP response (ideally `200 OK`).

**Execution date/time:** Pending  
**Actual result:** Pending  
**curl exit code:** Pending  
**Status:** Not Run  
**Evidence reference:** Pending  
**Interpretation:** Pending execution.

### T2 — Fake HTTP Wiki

**Objective:** Show that a client can receive a response from an attacker-controlled wiki simulation over HTTP without TLS-based proof of server identity.

**Planned command:**

```bash
curl -i http://wiki.internal.local:8081/
```

**Expected result:** The fake wiki returns an HTTP response (ideally `200 OK`). The client explicitly targets the simulated fake endpoint; this is not a demonstration of traffic interception or automatic redirection.

**Execution date/time:** Pending  
**Actual result:** Pending  
**curl exit code:** Pending  
**Status:** Not Run  
**Evidence reference:** Pending  
**Interpretation:** Pending execution.

### T3 — Legitimate HTTPS Wiki with Trusted CA

**Objective:** Verify that the client accepts the legitimate wiki's CA-signed certificate when the chain and requested hostname are valid.

**Planned command:**

```bash
curl -v --cacert ca/rootCA.crt https://wiki.internal.local:8443/
```

**Expected result:** Certificate chain and hostname verification succeed, followed by a successful HTTP response from the wiki. Certificate verification must remain enabled.

**Execution date/time:** Pending  
**Actual result:** Pending  
**curl exit code:** Pending  
**Status:** Not Run  
**Evidence reference:** Pending  
**Interpretation:** Pending execution.

### T4 — Fake HTTPS Wiki with Untrusted Certificate

**Objective:** Confirm that a verified TLS client rejects an impersonating HTTPS endpoint whose certificate does not chain to the trusted internal CA.

**Planned command:**

```bash
curl -v --cacert ca/rootCA.crt https://wiki.internal.local:9443/
```

**Expected result:** TLS certificate verification rejects the server certificate (often curl exit code `60`; diagnostic wording can vary). A mere connection refusal is not sufficient evidence.

**Execution date/time:** Pending  
**Actual result:** Pending  
**curl exit code:** Pending  
**Status:** Not Run  
**Evidence reference:** Pending  
**Interpretation:** Pending execution.

### T5 — Hostname Mismatch

**Objective:** Confirm that a certificate signed by the trusted internal CA is rejected if it does not identify the hostname or IP address requested by the client.

**Planned command:**

```bash
curl -v --cacert ca/rootCA.crt https://127.0.0.1:8443/
```

**Expected result:** Hostname/IP verification fails, **provided that** the certificate on port 8443 is valid for `wiki.internal.local` but does not include `127.0.0.1` as an IP Subject Alternative Name. The server must be reachable at `127.0.0.1:8443` and present that trusted-CA certificate.

**Execution date/time:** Pending  
**Actual result:** Pending  
**curl exit code:** Pending  
**Status:** Not Run  
**Evidence reference:** Pending  
**Interpretation:** Pending execution.

### T6 — Certificate Issued by Unrelated CA

**Objective:** Confirm that a certificate issued by a different, untrusted CA is rejected even when its hostname matches the requested service.

**Planned command:**

```bash
curl -v --cacert ca/rootCA.crt https://wiki.internal.local:9444/
```

**Expected result:** Certificate chain verification rejects the certificate issued by the unrelated CA (often curl exit code `60`). The separate endpoint on port 9444 must be running and present an unrelated-CA certificate with `wiki.internal.local` in its SAN, so this test isolates CA trust rather than hostname mismatch.

**Execution date/time:** Pending  
**Actual result:** Pending  
**curl exit code:** Pending  
**Status:** Not Run  
**Evidence reference:** Pending  
**Interpretation:** Pending execution.

## 5. Evidence Collection Procedure

For each test, record the execution timestamp, exact command, actual output, curl exit code, PASS/FAIL determination, and a short interpretation. Store relevant logs or screenshots in an agreed evidence location and reference them above. Do not include private keys, passphrases, or other secrets.

When running commands interactively, the exit code can be captured immediately afterward with:

```bash
printf 'curl exit code: %s\n' "$?"
```

Run that line immediately after the corresponding `curl` command, before any other command changes `$?`.

## 6. Pending Dependencies and Clarifications

- Confirm proposed hostnames, ports, and certificate file paths with Members 1 and 2.
- Make sure the legitimate and simulated services are running before recording results.
- Obtain the team's trusted root CA certificate for integrated verification.
- Clarify with the TA whether the separate “untrusted client” requirement refers to server-certificate rejection or mutual TLS (mTLS) client authentication; server-only TLS does not authenticate clients.
- Execute T1–T6 and replace every pending field with observed evidence.
- Review final results with Member 4 for report and presentation integration.

## 7. Results Interpretation (Complete After Testing)

**Observed findings:** Pending.  
**Deviations from expected results:** Pending.  
**Conclusion:** Pending execution and evidence review.

---

*This file is a pre-execution results template. No tests are claimed as completed.*
