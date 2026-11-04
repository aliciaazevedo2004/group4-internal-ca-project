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
7. How to start the HTTPS services
8. How to configure client trust
9. How to run each security test
10. Expected success and failure results
11. Known limitations and whether mTLS is implemented
12. Private-key handling and repository safety



