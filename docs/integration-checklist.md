Integration Checklist

This checklist will be used to verify that the Internal Certificate Authority project is organized, consistent, and reproducible before submission.

1. Certificate Authority and Certificates

- [ ] Root CA has been created and verified.
- [ ] Root CA public certificate is available to project members.
- [ ] Separate certificates have been generated for the internal wiki and API.
- [ ] Service certificates include the correct Subject Alternative Names (SANs).
- [ ] Private keys are not included in the GitHub repository.

2. Service Configuration

- [ ] Internal wiki HTTP baseline is working.
- [ ] Internal API HTTP baseline is working.
- [ ] HTTPS has been configured for the internal wiki.
- [ ] HTTPS has been configured for the internal API.
- [ ] Service hostnames and ports are documented consistently.

3. Client Trust and Verification

- [ ] Clients explicitly trust the Root CA certificate.
- [ ] Clients successfully connect to the legitimate wiki over HTTPS.
- [ ] Clients successfully connect to the legitimate API over HTTPS.
- [ ] Clients reject an untrusted or fake server certificate.
- [ ] Hostname verification is enabled.
- [ ] No insecure options are used to bypass certificate verification.

4. Security Testing

- [ ] HTTP baseline behavior has been demonstrated.
- [ ] Legitimate HTTPS connections have been demonstrated.
- [ ] An untrusted server connection has been rejected.
- [ ] Hostname verification has been tested.
- [ ] Untrusted client behavior has been tested, if applicable.
- [ ] Test results and supporting evidence are documented.
- [ ] Demonstrate that a client can connect to the fake wiki over the unprotected HTTP baseline.
- [ ] Demonstrate that a properly configured HTTPS client rejects an impersonator presenting an untrusted certificate.

5. Repository and Documentation

- [X] Main README includes setup and execution instructions.
- [X] Repository folders are organized and documented.
- [ ] Required scripts and configuration files are included.
- [X] No private keys, passwords, or other secrets are committed.
- [ ] Hostnames and ports match across documentation, certificates, services, and tests.
- [ ] A clean checkout of the repository has been tested.
- [ ] All required screenshots, logs, and test evidence are organized.

6. Final Project Preparation

- [ ] Report includes the system description and threat model.
- [ ] Report explains the security mechanisms and their purpose.
- [ ] Report includes test results and conclusions.
- [ ] AI Appendix is prepared.
- [ ] Presentation and demonstration order are finalized.
- [ ] Backup evidence is available in case the live demonstration fails.


