# group4-internal-ca-project

This is the Internal Certificate Authority project for Group 4.


1. Project purpose and security goals:

This project will establish an internal Public Key Infrastructure (PKI) for a small office network that contains tow internal web services, which consists of an internal wiki and an internal API.

The project will use a self-signed Root Certificate Authority (CA) to issue certificated for the services. The TLS will be configured to be able to protect any communication between clients and the project's legitimated services. 

The main security goals are:
- Authentication: Allowing clients to verify the identities of internal services.
- Confidentiality: Protecting transmitted information from network eavesdroppers.
- Integrity: Protecting communications from unauthorized changes.
- Service impersonation prevention: Preventing unauthorized hosts from attempting to impersonate real internal services.

2. Threat Model and Assumptions

The attacker is assumed to be an unauthorized host that has connected themselves to the internal network. They could be a compromised employee workstation or a rouge device.

The attacker's assumed abilities:
- Able to communicate with internal services
- Able to capture netwok traffic
- Able to host a fake version of an existing internal service
- Able to impersonate the existing legitimate wiki or API

The attacker is assumed not to to have:
- Access to the Root CA private key
- Any ability to modify the trusted CA configuration on client machines
- Administrative authority over the existing legitimate services

3. Architecture and host name/port table

The system contains these components:
- Internal Root Certificate Authority
- Internal Wiki
- Internal API
- A client that is configured to trust the internal Root CA
- Attacker-controlled host to be used for security testing

The Root CA will issue separate certificates for the wiki and API. Clients will use the trusted Root CA to validate the certificates that are presented by the services.

*Service configuration is to be determined*

4. Prerequisites and VM network setup

The project will use an internal network environment to host the services and perform security testing.

The expected tools and requirements will include the following:
- OpenSSL for certificate generation and verification
- A virtual machine that will be used to host and test services
- A client that is capable of msaking HTTPS requests
- curl for testing client connections
- Network connectivity between the client and internal services

*Certain configurations between the VM, operating systems, network settings, and intallation instructions are yet to be added.*

5. How to generate the root CA and leaf certificates

The project will use an OpenSSL to create a self-signed Root Certificate Authority, which will issue separate X.509 certificates for the following:
- The internal Wiki
- The internal API

Each service certificate must include the appropriate Subject Alternative Names (SANs) for verification of the hostname.

Certificate generation commands: *To be added*

For the safety of the Root CA private key, it will not be committed to the public repository.

6. How to start the HTTP baseline

The original system uses plain HTTP without encryption or certificate-based server identity verification.

The HTTP baseline will be used to demonstrate the security weaknesses of the original configuration, including the possibility of connecting to an unauthorized fake service.

Startup commands: TBD

7. How to start the HTTPS services

After certificate generation, the internal wiki and API will be configured to use HTTPS with their respective CA-signed certificates.

Each service should present its own certificate during TLS connections.

Startup commands: TBD

8. How to configure client trust

Clients must explicitly trust the internal Root CA and validate the certificate chain and hostname.

Certificate verification must remain enabled. Clients must not bypass certificate warnings or disable verification.

An example client request using curl is:

curl --cacert rootCA.crt https://<WIKI_HOSTNAME>:<WIKI_PORT>/

For the API:

curl --cacert rootCA.crt https://<API_HOSTNAME>:<API_PORT>/health

The certificate filename, hostnames, ports, and API endpoint are yet to be updated to match the final implementation.

9. How to run each security test

9. How to Run Each Security Test

The project will include security tests demonstrating the difference between the original HTTP configuration and the protected HTTPS configuration.

Planned tests include:

HTTP Impersonation: Demonstrate that a client can connect to a fake service over HTTP without verifying the server's identity.

Untrusted Certificate: Demonstrate that a client rejects a fake HTTPS service presenting a certificate not signed by the trusted Root CA.

Hostname Mismatch: Demonstrate that a client rejects a certificate that does not match the requested hostname.

Unrelated Certificate Authority: Demonstrate that a client rejects a certificate issued by an untrusted CA.

Legitimate Service Verification: Demonstrate that a properly configured client successfully connects to the legitimate wiki and API.

Test scripts and exact execution commands will be added after security testing is implemented.

10. Expected success and failure results

Tests:
1. Connect to fake service over HTTP
2. Connect to legitimate HTTPS service
3. Connect to fake HTTPS service with untrusted certificate
4. Connect with hostname mismatch
5. Connect using an unrelated CA

Expected test results listed respective of the above tests:
1. Connection may succeed without identity verification
2. Successful connection
3. Connection rejected
4. Connection rejected
5. Connection rejected

The expected results demonstrate that certificate validation allows clients to distinguish legitimate internal services from unauthorized impersonators.

11. Known limitations and whether mTLS is implemented

The project focuses primarily on server authentication using an internal Root CA and TLS.

Mutual TLS (mTLS), which requires clients to present acceptable certificates in addition to verifying the server, was identified as a possible additional security feature in the project proposal.

Final mTLS implementation status: TBD.

Additional limitations will be documented after implementation and testing.

12. Private-key handling and repository safety

Private keys and sensitive configuration files must never be committed to the public GitHub repository.

The .gitignore file excludes common sensitive file extensions: *.key, *.pem, *.p12, .env

The Root CA private key must be protected with restrictive file permissions and kept separate from the web servers.

Public certificates and safe configuration templates may be included when appropriate. Private keys must remain securely stored outside the public repository.

