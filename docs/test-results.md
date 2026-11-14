# Member 3 — Security Test Results

## 1. Proposed Lab Configuration

The following addresses are used for Member 3's isolated, loopback-only test environment. The legitimate HTTP wiki endpoint was confirmed during T1; the complete team HTTPS configuration still requires integration confirmation.

| **Component** | **Address** | **Purpose** |
| --- | --- | --- |
| Legitimate HTTP wiki | `http://wiki.internal.local:8080/` | HTTP baseline |
| Fake HTTP wiki | `http://wiki.internal.local:8081/` | Controlled impersonation simulation |
| Legitimate HTTPS wiki | `https://wiki.internal.local:8443/` | Trusted server certificate |
| Fake HTTPS wiki | `https://wiki.internal.local:9443/` | Untrusted certificate |
| Unrelated-CA HTTPS endpoint | `https://wiki.internal.local:9444/` | Certificate issued by another CA |

**Proposed local hostname mapping:** `127.0.0.1 wiki.internal.local` in `/etc/hosts`. The mapping to `127.0.0.1` was confirmed during T1 and earlier certificate testing.

**Tools:** `curl`, OpenSSL, and local test services. The `ca/rootCA.crt` path below is provisional and must be confirmed against the team's repository. Tests are limited to authorized project systems. Private keys and passphrases must not appear in evidence or be committed to the public repository.

The separate legitimate API is part of the overall project, but the six mandatory Member 3 test cases below focus on the wiki. API validation can be documented separately during integration.

## 2. Test Summary

| **ID** | **Scenario** | **Expected result** | **Actual result** | **Status** |
| --- | --- | --- | --- | --- |
| T1 | Legitimate wiki over HTTP | HTTP response received | Legitimate wiki returned HTTP `200 OK` and accessible page content | **PASS** |
| T2 | Fake wiki over HTTP | HTTP response received | Fake HTTP wiki returned HTTP `200 OK` over loopback | **PASS** |
| T3 | Legitimate wiki over verified HTTPS | Trusted certificate and hostname accepted | Awaiting legitimate HTTPS service and team root CA | Not Run |
| T4 | Fake HTTPS server with untrusted certificate | Certificate validation rejects connection | TLS handshake completed; curl rejected the self-signed certificate with exit code `60` | **PASS — self-signed rejection; team-CA check pending** |
| T5 | Trusted-CA certificate with incorrect hostname | Hostname verification rejects connection | Awaiting legitimate CA-signed HTTPS service | Not Run |
| T6 | Certificate issued by unrelated CA | Certificate chain verification rejects connection | Unrelated-CA certificate rejected by curl (exit `60`); team-CA check pending | **PASS — preliminary** |

A test is **PASS** only when observed behavior matches its expected result. T4's demonstrated **self-signed certificate rejection passed**; the separate integration check with the team's root CA has **not** been performed. Connection failures due to a stopped server, incorrect port, or DNS issue do not count as successful certificate-rejection tests.

## 3. Individual Test Records

### **T1 — Legitimate HTTP Wiki**

- **URL:** `http://wiki.internal.local:8080/`
- **Expected Result:** The legitimate wiki should be accessible over HTTP and return HTTP 200 OK.
- **Actual Result:** The legitimate wiki successfully returned HTTP 200 OK, and the page content was accessible.
- **Status:** PASS
- **curl exit code:** `0` (from saved evidence command; confirm against evidence file)
- **Evidence:**
  - `docs/evidence/t1-legitimate-http.txt`
  - `docs/evidence/t1-legitimate-http.png`

**Conclusion:** The legitimate internal wiki is accessible over HTTP. This establishes the baseline connection before testing HTTPS certificate validation.

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
**Evidence reference:** `docs/evidence/t2-fake-http.txt` and `docs/evidence/t2-fake-http.png` (confirm both files are present before submission).  
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
**Evidence reference:** `docs/evidence/t4-self-signed-rejection.txt` and `docs/evidence/t4-self-signed-rejection.png` (verify files correspond to the recorded test).  
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

**Command executed:**

`curl -v --max-time 10 --noproxy '*' https://wiki.internal.local:9444/`

**Expected result:** Certificate chain verification rejects the certificate issued by the unrelated CA, typically with curl exit code `60`.

**Execution date/time:** November 8, 2026 (local date; exact time not recorded).

**Actual result:** The unrelated-CA HTTPS server successfully completed a TLS 1.3 handshake. The server presented a certificate for `wiki.internal.local` issued by `Group4-Unrelated-Test-CA`. The hostname matched, but curl rejected the certificate chain because the issuing CA was not trusted.

**curl exit code:** `60`

**Status:** PASS — Unrelated CA rejection confirmed using the default trust store; verification against the team's internal root CA remains pending.

**Evidence reference:** `docs/evidence/t6-unrelated-ca-rejection.txt` and `docs/evidence/t6-unrelated-ca-rejection.png` (verify files are present; the screenshot was previously deleted locally).

**Interpretation:** The client rejected an HTTPS certificate issued by an untrusted CA despite successful hostname matching. This demonstrates that valid hostname information and a CA signature alone are insufficient; the certificate chain must terminate at a trusted CA.

## 4. Evidence Collection Procedure

For each test, record the execution timestamp, exact command, actual output, curl exit code, PASS/FAIL determination, and a short interpretation. Store relevant logs or screenshots in an agreed evidence location and reference them above. Do not include private keys, passphrases, or other secrets.

When running commands interactively, capture the exit code immediately afterward:

```bash
printf 'curl exit code: %s\n' "$?"
```

Run this line immediately after the corresponding `curl` command, before any other command changes `$?`.

## 5. Pending Dependencies and Clarifications

- Obtain Member 1's **public** trusted root CA certificate and confirm its actual repository path. Do not request or commit the CA private key.
- Confirm legitimate wiki hostnames, ports, and service availability with Members 1 and 2.
- T1 is complete. Run T3 and T5 when the legitimate HTTPS wiki and team CA are available.
- Repeat the **team-CA-specific T4 command** using `--cacert` once the public root CA certificate is available; the self-signed rejection already observed remains valid.
- T6 preliminary rejection was observed with the default trust store; repeat with the team root CA using `--cacert` once it is available. Verify regenerated T6 certificates and evidence still match the recorded run.
- Verify T1, T2, T4, and T6 evidence filenames and contents, save any missing logs or screenshots, and avoid including private keys or secrets.
- Clarify with the TA whether the separate “untrusted client” requirement refers to server-certificate rejection or mutual TLS (mTLS) client authentication; server-only TLS does not authenticate clients.
- Review final results with Member 4 for report and presentation integration.

## 6. Results Interpretation

**Observed findings:** T1 confirmed that the legitimate internal wiki was accessible over HTTP and returned `200 OK`. T2 confirmed that the simulated fake HTTP wiki returned `200 OK` over loopback. T4 confirmed that curl rejected a self-signed HTTPS certificate despite a matching hostname, returning exit code `60`. T6 confirmed that curl rejected a certificate issued by an unrelated, untrusted CA with exit code `60` using the default trust store.

**Deviations from expected results:** The initial T1 attempt failed because the legitimate service was unavailable, and a later attempt failed due to missing local hostname resolution. After the wiki service was started and `/etc/hosts` was updated, T1 succeeded. Earlier TLS troubleshooting timeouts were not counted as successful certificate-rejection tests. T3 and T5 remain not run. Team-root-CA-specific verification for T4 and T6 remains pending.

**Conclusion:** **T1, T2, T4, and T6 passed their documented preliminary scenarios.** T3 and T5 remain pending until the legitimate HTTPS service and trusted internal CA certificate are available. Full team integration testing is still required before all six scenarios can be considered complete.

---

*This document distinguishes observed preliminary results from outstanding integration checks. It does not claim that all six tests are complete.*
