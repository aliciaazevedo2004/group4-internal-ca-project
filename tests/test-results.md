# Security Test Results

**Project:** Internal Certificate Authority, Group 4  
**Member 3:** Security Testing

## Test 1: Fake HTTP Wiki

**Purpose:** Demonstrate that HTTP does not verify server identity.

**Expected Result:** The fake HTTP wiki accepts connections without certificate verification.

**Actual Result:** The fake HTTP wiki running on port `8081` returned `HTTP 200 OK`. Curl exited with code `0`, confirming that the connection succeeded without certificate verification.

**Status:** PASS

**Evidence:** `tests/evidence/t1-fake-http.txt`

## Test 2: Legitimate HTTPS Wiki

**Purpose:** Verify that the legitimate wiki is trusted using the internal Root CA.

**Expected Result:** The HTTPS connection succeeds with valid certificate-chain and hostname verification.

**Actual Result:** The legitimate HTTPS wiki running on port `8443` returned `HTTP 200 OK`. Curl exited with code `0` using the team's internal Root CA certificate. Certificate-chain and hostname verification remained enabled.

During Windows testing, the `--ssl-revoke-best-effort` option was used to accommodate unavailable certificate revocation information without disabling certificate-chain or hostname verification.

**Status:** PASS

**Evidence:** `tests/evidence/t2-legitimate-https.txt`

## Test 3: Fake HTTPS Wiki

**Purpose:** Verify that a fake HTTPS wiki with an untrusted certificate is rejected.

**Expected Result:** The connection fails certificate verification when using the team's internal Root CA.

**Actual Result:** The fake HTTPS wiki running on port `9443` presented a self-signed certificate that was not issued by the trusted Root CA. Curl rejected the connection with exit code `60`. Windows Schannel reported that the certificate chain was based on an untrusted root.

**Status:** PASS

**Evidence:** `tests/evidence/t3-self-signed-rejection.txt`

## Test Summary

| Test | Result | Status |
|---|---|---|
| Test 1: Fake HTTP | HTTP 200; curl exit 0 | PASS |
| Test 2: Legitimate HTTPS | Trusted HTTPS; curl exit 0 | PASS |
| Test 3: Fake HTTPS | Untrusted certificate; curl exit 60 | PASS |

**Final Automated Test Results:**

- Tests Passed: 3
- Tests Failed: 0
- Overall Status: ALL TESTS PASSED

## Conclusion

All three automated security tests passed successfully. The fake HTTP wiki accepted connections without certificate verification, while the legitimate HTTPS wiki established a trusted connection using the internal Root CA.

The fake HTTPS wiki was rejected because its certificate was not issued by the trusted Root CA. These results demonstrate that certificate verification helps clients distinguish legitimate internal services from impersonating services presenting untrusted certificates.

The automated testing script, `tests/security_tests.sh`, records the test outcomes and saves supporting logs in the `tests/evidence/` directory.
