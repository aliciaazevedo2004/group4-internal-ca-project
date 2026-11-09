# Member 3 — Security Test Results

## 2. Proposed Lab Configuration

The following values are proposed for Member 3's isolated, loopback-only test environment and are **not yet confirmed as the team's final service configuration**.

| **Component** | **Address** | **Purpose** |
| --- | --- | --- |
| Legitimate HTTP wiki | `http://wiki.internal.local:8080/` | HTTP baseline |
| Fake HTTP wiki | `http://wiki.internal.local:8081/` | Controlled impersonation simulation |
| Legitimate HTTPS wiki | `https://wiki.internal.local:8443/` | Trusted server certificate |
| Fake HTTPS wiki | `https://wiki.internal.local:9443/` | Untrusted certificate |
| Unrelated-CA HTTPS endpoint | `https://wiki.internal.local:9444/` | Certificate issued by another CA |

**Proposed local hostname mapping:** `127.0.0.1 wiki.internal.local` in `/etc/hosts`. The mapping to `127.0.0.1` was confirmed during the T4 test.

**Tools:** `curl`, OpenSSL, and local test services. The `ca/rootCA.crt` path below is provisional and must be confirmed against the team's repository. Tests are limited to authorized project systems. Private keys and passphrases must not appear in evidence or be committed to the public repository.

The separate legitimate API is part of the overall project, but the six mandatory Member 3 test cases below focus on the wiki. API validation can be documented separately during integration.

## 3. Test Summary

| **ID** | **Scenario** | **Expected result** | **Actual result** | **Status** |
| --- | --- | --- | --- | --- |
| T1 | Legitimate wiki over HTTP | HTTP response received | Connection to the proposed legitimate HTTP endpoint failed while the service was unavailable | Blocked |
| T2 | Fake wiki over HTTP | HTTP response received | Fake HTTP wiki returned HTTP `200 OK` over loopback | **PASS** |
| T3 | Legitimate wiki over verified HTTPS | Trusted certificate and hostname accepted | Awaiting legitimate HTTPS service and team root CA | Not Run |
| T4 | Fake HTTPS server with untrusted certificate | Certificate validation rejects connection | TLS handshake completed; curl rejected the self-signed certificate with exit code `60` | **PASS — self-signed rejection; team-CA check pending** |
| T5 | Trusted-CA certificate with incorrect hostname | Hostname verification rejects connection | Awaiting legitimate CA-signed HTTPS service | Not Run |
| T6 | Certificate issued by unrelated CA | Certificate chain verification rejects connection | Awaiting unrelated-CA HTTPS endpoint and team root CA | Not Run |

A test is **PASS** only when observed behavior matches its expected result. T4's demonstrated **self-signed certificate rejection passed**; the separate integration check with the team's root CA has **not** been performed. Connection failures due to a stopped server, incorrect port, or DNS issue do not count as successful certificate-rejection tests.

## 4. Individual Test Records

### T1 — Legitimate HTTP Wiki

**Objective:** Establish that the legitimate wiki responds over HTTP without TLS-based server authentication.

**Planned command:**

```bash
curl -i http://wiki.internal.local:8080/
```

**Expected result:** The legitimate wiki returns an HTTP response (ideally `200 OK`).

**Execution date/time:** Earlier preliminary attempt; exact timestamp not recorded.  
**Actual result:** Curl failed to connect to the proposed legitimate wiki endpoint because the service was not running or reachable at that time. This is a service-availability blocker, not a failed HTTP security test.  
**curl exit code:** `7` (connection failure).  
**Status:** Blocked — retry when the legitimate wiki is running.  
**Evidence reference:** Preliminary terminal output; filename not confirmed.  
**Interpretation:** No conclusion can be drawn about the legitimate HTTP service until it is available.

### T2 — Fake HTTP Wiki

**Objective:** Show that a client can receive a response from an attacker-controlled wiki simulation over HTTP without TLS-based proof of server identity.

**Command executed during preliminary testing:**

```bash
curl -i http://127.0.0.1:8081/
```

**Planned hostname-based command (repeat only if required for final integration):**

```bash
curl -i http://wiki.internal.local:8081/
```

**Expected result:** The fake wiki returns an HTTP response (ideally `200 OK`). The client explicitly targets the simulated fake endpoint; this is not a demonstration of traffic interception or automatic redirection.

**Execution date/time:** Previously executed; exact timestamp not recorded.  
**Actual result:** The fake HTTP wiki was reachable on loopback port `8081` and returned HTTP `200 OK`.  
**curl exit code:** Not recorded.  
**Status:** **PASS — fake HTTP response confirmed.**  
**Evidence reference:** Previously captured terminal screenshot and response text; confirm final filenames before submission.  
**Interpretation:** The simulated wiki can serve content over HTTP without cryptographic proof of server identity. This test does not claim interception or redirection of traffic.

### T3 — Legitimate HTTPS Wiki with Trusted CA

**Objective:** Verify that the client accepts the legitimate wiki's CA-signed certificate when the chain and requested hostname are valid.

**Planned command:**

```bash
curl -v --cacert ca/rootCA.crt https://wiki.internal.local:8443/
```

**Expected result:** Certificate chain and hostname verification succeed, followed by a successful HTTP response from the wiki. Certificate verification must remain enabled.

**Execution date/time:** Pending.  
**Actual result:** Pending legitimate HTTPS service and team CA certificate.  
**curl exit code:** Pending.  
**Status:** Not Run.  
**Evidence reference:** Pending.  
**Interpretation:** Pending integration.

### T4 — Fake HTTPS Wiki with Untrusted Certificate

**Objective:** Confirm that a verified TLS client rejects an impersonating HTTPS endpoint whose certificate is not trusted.

**Command executed:**

```bash
curl -v --max-time 10 --noproxy '*' https://wiki.internal.local:9443/
echo "Exit code: $?"
```

**Planned team-CA integration command (not yet executed):**

```bash
curl -v --cacert ca/rootCA.crt https://wiki.internal.local:9443/
```

**Expected result:** TLS certificate verification rejects the fake server certificate (often curl exit code `60`). A connection refusal or handshake timeout does not satisfy the test.

**Execution date/time:** November 8, 2026, local date; exact time not recorded.  
**Actual result:** The hostname resolved to `127.0.0.1`. TLS 1.3 handshake completed. The server presented a self-signed certificate with `CN=wiki.internal.local`, and its Subject Alternative Name matched `wiki.internal.local`. With certificate verification enabled, curl rejected the certificate as self-signed.  
**Observed output:**

```text
subjectAltName: "wiki.internal.local" matches cert's "wiki.internal.local"
SSL certificate OpenSSL verify result: self-signed certificate (18)
curl: (60) SSL certificate OpenSSL verify result: self-signed certificate (18)
Exit code: 60
```

**curl exit code:** `60`.  
**Status:** **PASS — self-signed certificate rejection confirmed.** Team-CA-specific integration check pending.  
**Evidence reference:** Terminal output confirmed; `docs/evidence/t4-self-signed-rejection.txt` if the evidence-saving command was executed (verify file exists before final submission).  
**Interpretation:** A matching hostname is insufficient to establish certificate trust. Curl correctly rejected the fake HTTPS endpoint. Once Member 1 provides the public root CA certificate, repeat the test with `--cacert` to complete the team-specific integration requirement. The earlier TLS timeouts were troubleshooting failures, not the successful certificate-rejection result.

### T5 — Hostname Mismatch

**Objective:** Confirm that a certificate signed by the trusted internal CA is rejected if it does not identify the hostname or IP address requested by the client.

**Planned command:**

```bash
curl -v --cacert ca/rootCA.crt https://127.0.0.1:8443/
```

**Expected result:** Hostname/IP verification fails, **provided that** the certificate on port `8443` is valid for `wiki.internal.local` but does not include `127.0.0.1` as an IP Subject Alternative Name. The server must be reachable at `127.0.0.1:8443` and present that trusted-CA certificate.

**Execution date/time:** Pending.  
**Actual result:** Pending.  
**curl exit code:** Pending.  
**Status:** Not Run.  
**Evidence reference:** Pending.  
**Interpretation:** Pending integration.

### T6 — Certificate Issued by Unrelated CA

**Objective:** Confirm that a certificate issued by a different, untrusted CA is rejected even when its hostname matches the requested service.

**Planned command:**

```bash
curl -v --cacert ca/rootCA.crt https://wiki.internal.local:9444/
```

**Expected result:** Certificate chain verification rejects the certificate issued by the unrelated CA (often curl exit code `60`). The separate endpoint on port `9444` must be running and present an unrelated-CA certificate with `wiki.internal.local` in its SAN, so this test isolates CA trust rather than hostname mismatch.

**Execution date/time:** Pending.  
**Actual result:** Pending.  
**curl exit code:** Pending.  
**Status:** Not Run.  
**Evidence reference:** Pending.  
**Interpretation:** Pending integration.

## 5. Evidence Collection Procedure

For each test, record the execution timestamp, exact command, actual output, curl exit code, PASS/FAIL determination, and a short interpretation. Store relevant logs or screenshots in an agreed evidence location and reference them above. Do not include private keys, passphrases, or other secrets.

When running commands interactively, capture the exit code immediately afterward:

```bash
printf 'curl exit code: %s\n' "$?"
```

Run this line immediately after the corresponding `curl` command, before any other command changes `$?`.

## 6. Pending Dependencies and Clarifications

- Obtain Member 1's **public** trusted root CA certificate and confirm its actual repository path. Do not request or commit the CA private key.
- Confirm legitimate wiki hostnames, ports, and service availability with Members 1 and 2.
- Run T1 when the legitimate HTTP wiki is available; run T3 and T5 when the legitimate HTTPS wiki and team CA are available.
- Repeat the **team-CA-specific T4 command** using `--cacert` once the public root CA certificate is available; the self-signed rejection already observed remains valid.
- Configure and test T6's separate unrelated-CA HTTPS endpoint, using a certificate with a matching hostname.
- Verify T2 and T4 evidence filenames, save any missing logs, and avoid including private keys or secrets.
- Clarify with the TA whether the separate “untrusted client” requirement refers to server-certificate rejection or mutual TLS (mTLS) client authentication; server-only TLS does not authenticate clients.
- Review final results with Member 4 for report and presentation integration.

## 7. Results Interpretation

**Observed findings:** T2 confirmed that the simulated fake HTTP wiki returned HTTP `200 OK` over loopback. T4 confirmed that a TLS handshake completed with the fake HTTPS wiki and that curl rejected its self-signed certificate despite a matching hostname, returning exit code `60`.

**Deviations from expected results:** No unexpected behavior was observed in the successful T2 and T4 checks. Earlier TLS handshake timeouts were resolved sufficiently to complete the T4 certificate-rejection check. T1 could not be completed because the legitimate service was unavailable. T3, T5, and T6 have not been run, and the team-CA-specific T4 integration check remains pending.

**Conclusion:** The completed checks demonstrate that an HTTP endpoint can return content without cryptographic server authentication and that an HTTPS client can reject an untrusted certificate even when its hostname matches. **T2 passed; T4's self-signed certificate rejection passed.** Full team integration testing remains necessary before claiming all six scenarios are complete.

---

*This document records observed preliminary results and clearly identifies outstanding integration checks. It is not a claim that all six tests have been completed.*
