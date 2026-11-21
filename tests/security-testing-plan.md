# Security Testing Plan

**Project:** Internal Certificate Authority, Group 4  
**Member 3:** Security Testing

## Objective

Demonstrate how HTTPS and a trusted Certificate Authority (CA) protect internal services from server impersonation.

## Test 1: Fake HTTP Wiki

**Purpose:** Show that HTTP does not verify the server's identity.

**Command:**
```bash
curl -i http://127.0.0.1:8081/
```

**Expected Result:** Connection succeeds without certificate verification.

**Status:** PASS

## Test 2: Legitimate HTTPS Wiki

**Purpose:** Verify that the legitimate wiki is trusted using our internal CA.

**Command:**
```bash
curl --noproxy '*' \
  --resolve wiki.internal.local:8443:127.0.0.1 \
  --cacert ca/rootCA.crt \
  --ssl-revoke-best-effort \
  https://wiki.internal.local:8443/
```

**Expected Result:** Secure HTTPS connection succeeds with certificate-chain and hostname verification enabled.

**Actual Result:** The legitimate HTTPS wiki returned HTTP 200 OK with curl exit code 0.

**Status:** PASS

## Test 3: Fake HTTPS Wiki

**Purpose:** Verify that an untrusted certificate is rejected.

**Command:**
```bash
curl --noproxy '*' \
  --resolve wiki.internal.local:9443:127.0.0.1 \
  --cacert ca/rootCA.crt \
  --ssl-revoke-best-effort \
  https://wiki.internal.local:9443/
```

**Expected Result:** Certificate verification fails with curl error 60.

**Actual Result:** The fake HTTPS wiki was rejected with curl error 60 because its certificate was not issued by the trusted Root CA.

**Status:** PASS

## Test Summary

| Test | Expected Result | Status |
|---|---|---|
| Test 1: Fake HTTP | Connection accepted | PASS |
| Test 2: Legitimate HTTPS | Trusted connection accepted | PASS |
| Test 3: Fake HTTPS | Untrusted connection rejected | PASS |

**Final Results:** 3 tests passed, 0 failed.

## Conclusion

All three security tests passed. The fake HTTP wiki accepted connections without certificate verification, the legitimate HTTPS wiki established a trusted connection using our internal Root CA, and the fake HTTPS wiki was rejected because its certificate was untrusted.

These results demonstrate how certificate verification helps clients distinguish legitimate internal services from fake services attempting to impersonate them.
