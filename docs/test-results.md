# Security Test Results

**Project:** Internal Certificate Authority Setup for a Small Network  
**Team:** Group 4  
**Tester:** Diya Patel — Attack Demonstration and Security Testing  
**Status:** Testing not yet executed  
**Environment:** To be documented after setup

## 1. Testing Objective

Verify that the internal Certificate Authority (CA) protects the internal wiki and API by enabling encrypted HTTPS communication and validating server identities. Testing will compare the insecure HTTP baseline with the secured configuration and verify that invalid certificates and hostname mismatches are rejected.

## 2. Test Results Summary

| Test ID | Test Description | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| T1 | HTTP baseline | Service responds without authenticating server identity. | Not tested | Not Run |
| T2 | Fake HTTP service | Client cannot verify server identity using HTTP alone. | Not tested | Not Run |
| T3 | Trusted HTTPS | Connection succeeds with a valid certificate, matching hostname, and trusted team CA. | Not tested | Not Run |
| T4 | Untrusted certificate | Client rejects the certificate. | Not tested | Not Run |
| T5 | Hostname mismatch | Client rejects the connection because the hostname does not match the certificate. | Not tested | Not Run |

## 3. Detailed Test Records

### T1 — HTTP Baseline

- **Purpose:** Establish the behavior of the service before TLS protection.
- **Setup:** Start the HTTP version of the internal wiki or API.
- **Command:** `curl -v http://<WIKI_HOST>:<HTTP_PORT>/`
- **Expected result:** The service responds, but HTTP does not authenticate the server's identity or encrypt the connection.
- **Actual result:** Not tested.
- **Status:** Not Run.
- **Evidence:** `evidence/T1-http-baseline.png` (to be captured).

### T2 — Fake HTTP Service

- **Purpose:** Demonstrate the risk of service impersonation over HTTP.
- **Setup:** Run a clearly labeled fake service in the authorized, isolated project lab.
- **Procedure:** Connect to the fake service using HTTP and compare the response with the legitimate service.
- **Expected result:** HTTP provides no cryptographic proof that the responding service is legitimate.
- **Actual result:** Not tested.
- **Status:** Not Run.
- **Evidence:** `evidence/T2-fake-http-service.png` (to be captured).

### T3 — Trusted HTTPS

- **Purpose:** Verify that a legitimate service is accessible over HTTPS when its certificate is trusted and its hostname matches.
- **Setup:** Use the team's root CA certificate and the configured HTTPS service.
- **Command:** `curl --cacert <ROOT_CA_CERT> https://<WIKI_HOST>:<HTTPS_PORT>/`
- **Expected result:** The connection succeeds with certificate and hostname verification enabled.
- **Actual result:** Not tested.
- **Status:** Not Run.
- **Evidence:** `evidence/T3-trusted-https.png` (to be captured).

### T4 — Untrusted Certificate

- **Purpose:** Verify that the client rejects a certificate that is not trusted by the team's CA.
- **Setup:** Use a controlled test server whose certificate is not signed by the trusted team CA.
- **Command:** `curl --cacert <ROOT_CA_CERT> https://<TEST_HOST>:<TEST_PORT>/`
- **Expected result:** Certificate verification fails and the client does not establish a successfully verified HTTPS connection.
- **Actual result:** Not tested.
- **Status:** Not Run.
- **Evidence:** `evidence/T4-untrusted-certificate.png` (to be captured).

### T5 — Hostname Mismatch

- **Purpose:** Verify that the client rejects a certificate that is trusted but does not match the requested hostname.
- **Setup:** Connect using a hostname that does not match the certificate's Subject Alternative Name (SAN).
- **Command:** `curl --cacert <ROOT_CA_CERT> https://<WRONG_HOSTNAME>:<HTTPS_PORT>/`
- **Expected result:** Hostname verification fails, even if the certificate chain is trusted.
- **Actual result:** Not tested.
- **Status:** Not Run.
- **Evidence:** `evidence/T5-hostname-mismatch.png` (to be captured).

## 4. Evidence and Environment

Record the following once the project is running:

- Operating system or course VM used:
- Service software and versions:
- Wiki hostname and ports:
- API hostname and ports:
- Root CA certificate path:
- Date testing was performed:
- Git commit tested:

Store terminal output and screenshots in the project's `evidence/` directory. Do not include private keys or other secrets in screenshots or commits.

## 5. Issues and Follow-Up

| Issue | Impact | Action Taken | Status |
|---|---|---|---|
| Official hostnames and ports not yet confirmed | Tests cannot be executed with final settings | Coordinate with service and CA team members | Open |
| Services and certificates not yet available | End-to-end testing is blocked | Execute tests after integration | Open |

## 6. Final Assessment

**Pending testing.** No security conclusions can be confirmed until the tests have been executed against the integrated project. After testing, update each result with the actual outcome, mark it Pass or Fail, and explain any unexpected behavior.

A passing test indicates that the observed behavior matched the expected result for that specific test; it does not, by itself, prove the entire system is secure.
