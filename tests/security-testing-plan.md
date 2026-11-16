# Security Testing Plan

**Project:** Internal Certificate Authority — Group 4  
**Member 3:** Security Testing

## Objective

Demonstrate how HTTPS and a trusted Certificate Authority (CA) protect internal services from server impersonation.

## Test 1 — Fake HTTP Wiki

**Purpose:** Show that HTTP does not verify the server's identity.

**Command:**
```bash
curl -i http://127.0.0.1:8081/
```

**Expected Result:** Connection succeeds without certificate verification.

**Status:** PASS (previously T2)

## Test 2 — Legitimate HTTPS Wiki

**Purpose:** Verify that the legitimate wiki is trusted using our internal CA.

**Command:**
```bash
curl --noproxy '*' \
  --resolve wiki.internal.local:8443:127.0.0.1 \
  --cacert ca/rootCA.crt \
  https://wiki.internal.local:8443/
```

**Expected Result:** Secure HTTPS connection succeeds.

**Status:** Pending (previously T3)

## Test 3 — Fake HTTPS Wiki

**Purpose:** Verify that an untrusted certificate is rejected.

**Command:**
```bash
curl --noproxy '*' \
  --resolve wiki.internal.local:9443:127.0.0.1 \
  --cacert ca/rootCA.crt \
  https://wiki.internal.local:9443/
```

**Expected Result:** Certificate verification fails (curl error 60).

**Status:** PASS

## Test Summary

| Test | Expected Result | Status |
|---|---|---|
| Test 1 — Fake HTTP | Connection accepted | PASS |
| Test 2 — Legitimate HTTPS | Trusted connection accepted | Pending |
| Test 3 — Fake HTTPS | Untrusted connection rejected | PASS |


## Conclusion

These three tests demonstrate that HTTP lacks certificate-based server authentication, legitimate HTTPS connections can be trusted, and fake HTTPS certificates are rejected.