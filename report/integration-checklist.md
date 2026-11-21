# Integration Checklist

**Project:** Internal Certificate Authority, Group 4  
**Course:** ITIS 3200

This checklist tracks the project's progress and ensures all components are ready for final submission.

## 1. Certificate Authority

- [x] Root CA public certificate is available in the repository.
- [x] Separate wiki and API certificates are available.
- [x] Private keys are excluded from GitHub.
- [x] Wiki and API certificate chains have been verified using OpenSSL.
- [ ] Subject Alternative Names (SANs) have been verified.
- [x] Matching private keys were available locally during testing.

## 2. Internal Services

- [x] Wiki and API service implementations are included.
- [x] HTTP and HTTPS ports are configured.
- [x] Legitimate wiki successfully runs over HTTPS.
- [ ] Legitimate API successfully runs over HTTPS.

## 3. Security Testing

- [x] Test 1: Fake HTTP Wiki, PASS.
- [x] Test 2: Legitimate HTTPS Wiki, PASS.
- [x] Test 3: Fake HTTPS Wiki, PASS.
- [x] Fake HTTPS certificate rejection verified using the internal Root CA.
- [x] Automated three-test script is included.
- [x] Final automated testing completed with 3 tests passed and 0 failed.

## 4. Documentation

- [x] Main README updated.
- [x] Security testing plan documented.
- [x] Test results documented.
- [x] Security testing scripts included.
- [x] Final security test evidence generated.
- [ ] Final evidence files reviewed and organized in GitHub.
- [ ] All documentation uses consistent paths and test names.

## 5. Final Report and Presentation

- [x] Final report drafted.
- [x] System architecture and security mechanisms explained.
- [x] Security testing results included.
- [x] AI usage appendix drafted.
- [ ] Final report reviewed and submitted in DOCX and PDF formats.
- [ ] Presentation slides completed.
- [ ] Live demonstration rehearsed.
- [ ] Individual contribution reflections completed.

## Final Status

The internal Root CA, service certificates, application code, and security testing scripts have been implemented. The legitimate HTTPS wiki was successfully verified, and all three automated security tests passed with zero failures.

The final report has been drafted and includes the system description, security mechanisms, implementation details, failure-case analysis, and security testing results.

Remaining work includes confirming the API's HTTPS operation, verifying certificate SANs, reviewing the final GitHub documentation and evidence, completing the presentation, and submitting the required deliverables.
