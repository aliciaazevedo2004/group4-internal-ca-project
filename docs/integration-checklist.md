# Integration Checklist

This checklist tracks the Internal Certificate Authority project's progress toward a consistent, secure, and reproducible final submission.

## 1. Certificate Authority and Certificates

- [ ] Root CA has been created and verified.
- [ ] Root CA public certificate is available to project members.
- [ ] Separate certificates have been generated for the internal wiki and API.
- [ ] Service certificates include the correct Subject Alternative Names (SANs).
- [x] Private keys are not included in the GitHub repository.

**Notes:** Member 1 has not yet provided the public root CA certificate. The legitimate wiki and API certificates have not been verified by Member 3. T4 and T6 test certificates are separate from the legitimate service certificates.

## 2. Service Configuration

- [x] Internal wiki HTTP baseline is working.
- [ ] Internal API HTTP baseline is working.
- [ ] HTTPS has been configured and successfully started for the internal wiki.
- [ ] HTTPS has been configured and successfully started for the internal API.
- [x] Service hostnames and ports are documented in the service configuration.

**Notes:** The legitimate HTTP wiki returned HTTP 200 OK during T1. The service code supports HTTPS, but the legitimate CA-signed certificates are not yet available for integration testing.

## 3. Client Trust and Verification

- [ ] Clients explicitly trust the Root CA certificate.
- [ ] Clients successfully connect to the legitimate wiki over HTTPS.
- [ ] Clients successfully connect to the legitimate API over HTTPS.
- [x] Clients reject an untrusted or fake server certificate.
- [ ] Hostname verification has been confirmed against the legitimate HTTPS service.
- [x] Certificate-rejection tests were performed without bypassing verification.

**Notes:** T4 demonstrated rejection of a self-signed certificate. T6 demonstrated rejection of an unrelated-CA certificate using the default trust store. Tests using the team's trusted root CA remain pending.

## 4. Security Testing

- [x] HTTP baseline behavior has been demonstrated.
- [ ] Legitimate HTTPS connections have been demonstrated.
- [x] An untrusted server connection has been rejected.
- [ ] Hostname mismatch rejection has been tested.
- [ ] Untrusted client behavior has been tested, if applicable.
- [x] Completed test results and supporting evidence are documented.
- [x] Demonstrated that a client can connect to the fake wiki over HTTP.
- [x] Demonstrated that an HTTPS client rejects an impersonator presenting an untrusted certificate.

**Notes:** T1, T2, T4, and T6 have passed their documented preliminary scenarios. T3 and T5 remain pending. Team-CA-specific checks for T4 and T6 remain outstanding.

## 5. Repository and Documentation

- [x] Main README includes setup and execution instructions.
- [x] Repository folders are organized and documented.
- [ ] Required scripts and configuration files are included and verified.
- [x] No private keys, passwords, or other secrets are committed.
- [ ] Hostnames and ports match across documentation, certificates, services, and tests.
- [ ] A clean checkout of the repository has been tested.
- [ ] All required screenshots, logs, and test evidence are organized.

**Notes:** The legitimate HTTPS certificate files are not present on the GitHub main branch. T1 evidence has been uploaded, but the complete evidence collection still requires final verification.

## 6. Final Project Preparation

- [ ] Report includes the system description and threat model.
- [ ] Report explains the security mechanisms and their purpose.
- [ ] Report includes test results and conclusions.
- [ ] AI Appendix is prepared.
- [ ] Presentation and demonstration order are finalized.
- [ ] Backup evidence is available in case the live demonstration fails.

**Notes:** Final report and presentation preparation remain to be confirmed by the group.

---

## Current Integration Summary

**Completed preliminary security tests:** T1, T2, T4, T6.

**Pending security tests:** T3, T5.

**Outstanding dependencies:** Member 1's public root CA certificate, legitimate CA-signed service certificates, HTTPS integration testing, API verification, and final documentation review.

**Overall status:** Integration in progress. The HTTP baseline and preliminary certificate-rejection demonstrations are complete, but full trusted-HTTPS integration has not yet been verified.