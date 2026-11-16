# Integration Checklist

**Project:** Internal Certificate Authority — Group 4  
**Course:** ITIS 3200

This checklist tracks the project's progress and ensures all components are ready for final submission.

## 1. Certificate Authority

- [x] Root CA public certificate is available in the repository.
- [x] Separate wiki and API certificates are available.
- [x] Private keys are excluded from GitHub.
- [ ] Certificate chains and Subject Alternative Names (SANs) have been verified.
- [ ] Matching private keys are available locally.

## 2. Internal Services

- [x] Wiki and API service implementations are included.
- [x] HTTP and HTTPS ports are configured.
- [ ] Legitimate wiki successfully runs over HTTPS.
- [ ] Legitimate API successfully runs over HTTPS.

## 3. Security Testing

- [x] Test 1 — Fake HTTP Wiki: PASS.
- [ ] Test 2 — Legitimate HTTPS Wiki: Pending verification.
- [ ] Test 3 — Fake HTTPS Wiki: Final Root CA verification pending.
- [x] Preliminary fake HTTPS certificate rejection demonstrated.
- [x] Automated three-test script is included.

## 4. Documentation

- [x] Main README updated.
- [x] Security testing plan documented.
- [x] Test results documented.
- [x] Security testing scripts included.
- [ ] Final test evidence reviewed and organized.
- [ ] All documentation uses consistent paths and test names.

## 5. Final Report and Presentation

- [ ] Final report completed.
- [ ] System architecture and security mechanisms explained.
- [ ] Security testing results included.
- [ ] AI usage appendix completed.
- [ ] Presentation slides completed.
- [ ] Live demonstration rehearsed.

## Final Status

The Root CA public certificate, service certificates, application code, and security testing scripts are available in the repository.

Test 1 has passed, and preliminary evidence confirms rejection of a self-signed HTTPS certificate. Final trusted-HTTPS integration and Root CA verification remain to be confirmed.

The remaining work includes completing verification, organizing final evidence, and finishing the report and presentation.
