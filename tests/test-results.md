# Security Test Results

**Project:** Internal Certificate Authority — Group 4  
**Member 3:** Security Testing

## Test 1 — Fake HTTP Wiki

**Purpose:** Demonstrate that HTTP does not verify server identity.

**Expected Result:** The fake HTTP wiki accepts connections without certificate verification.

**Actual Result:** The fake HTTP wiki returned `HTTP 200 OK` without certificate verification.

**Status:** PASS

**Evidence:** `tests/evidence/t1-fake-http.txt`

## Test 2 — Legitimate HTTPS Wiki

**Purpose:** Verify that the legitimate wiki is trusted using the internal Root CA.

**Expected Result:** The HTTPS connection succeeds with valid certificate and hostname verification.

**Actual Result:** Final integration result not yet recorded.

**Status:** PENDING

**Evidence:** To be added after verification.

## Test 3 — Fake HTTPS Wiki

**Purpose:** Verify that a fake HTTPS wiki with an untrusted certificate is rejected.

**Expected Result:** The connection fails certificate verification.

**Actual Result:** Curl rejected the self-signed certificate with error `60`. This was confirmed using the default trust store; the final test using the team's Root CA remains outstanding.

**Status:** PRELIMINARY PASS

**Evidence:** `tests/evidence/t3-self-signed-rejection.txt`

## Test Summary

| Test | Result | Status |
|---|---|---|
| Test 1 — Fake HTTP | HTTP connection accepted | PASS |
| Test 2 — Legitimate HTTPS | Awaiting final verification | PENDING |
| Test 3 — Fake HTTPS | Self-signed certificate rejected | PRELIMINARY PASS |

## Conclusion

The completed tests demonstrate that HTTP connections lack certificate-based server authentication and that clients reject untrusted HTTPS certificates.

Final verification of the legitimate HTTPS wiki and the fake HTTPS wiki against the team's Root CA is required before all three tests can be reported as passed.
