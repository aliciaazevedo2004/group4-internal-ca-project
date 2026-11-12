Internal Certificate Authority Project Report

*The report is yet to be filled, this is just an outline*

1. Introduction

- Purpose of the project:
- Overview of the small office network:
- Description of the internal wiki and API:
- Security goals: authenticity, confidentiality, and integrity:

2. System Description

- Existing HTTP configuration:
- Network environment and services:
- Users and assets requiring protection:
- System architecture:

3. Threat Model

- Description of the attacker:
- Attacker capabilities and limitations:
- Potential attack methods:
- Security properties at risk:

4. Security Mechanism Design

- Overview of Public Key Infrastructure (PKI):
- Internal Root Certificate Authority:
- Generation and management of service certificates:
- Subject Alternative Names (SANs) and hostname verification:
- TLS configuration for the wiki and API:
- Explicit client trust configuration:
- Mutual TLS (mTLS), if implemented:

5. Implementation

- Tools and technologies used:
- Repository organization:
- Root CA and certificate setup:
- Wiki and API configuration:
- Client trust configuration:
- Relevant commands and configuration files:

6. Security Testing and Demonstration

- HTTP baseline demonstration:
- Fake wiki / service impersonation demonstration:
- Legitimate HTTPS connection:
- Rejection of an untrusted certificate:
- Hostname verification testing:
- Test results and supporting evidence:

7. Results and Discussion

- Comparison of the original HTTP configuration and secured HTTPS configuration:
- How the implementation addresses the identified threats:
- Security benefits and limitations:
- Any implementation difficulties or unexpected results:

8. Conclusion

- Summary of project accomplishments:
- Whether the security goals were achieved:
- Lessons learned:
- Possible future improvements:

9. References

- Technical documentation:
- Tools and technologies referenced:
- Other sources used in the project:







