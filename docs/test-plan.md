# Security Testing Plan

## Objective
Verify that the internal Certificate Authority (CA) protects the group's internal wiki and API against unencrypted communication and server impersonation.

## Test Cases

| ID | Test | Expected Result |
|---|---|---|
| T1 | Connect to the HTTP baseline | Service responds, but the connection does not authenticate the server's identity. |
| T2 | Connect to a fake HTTP service in the isolated lab | HTTP alone cannot verify whether the service is legitimate. |
| T3 | Connect to the legitimate HTTPS service using the team's root CA certificate | Connection succeeds when the certificate chain and hostname are valid. |
| T4 | Connect to HTTPS using an untrusted certificate | Certificate verification fails. |
| T5 | Connect using a hostname that does not match the certificate | Hostname verification fails. |

## Evidence Collection
For each test, record:
- Test ID and date
- Setup and command used
- Expected result
- Actual result
- Pass/fail status
- Screenshot or terminal output

## Security Notes
Certificate verification must remain enabled. Do not bypass TLS warnings or disable certificate checks to make a test pass. Use only the group's authorized lab environment.

## Current Status
Tests are planned but have not yet been executed. Hostnames, ports, and commands will be added once the team finalizes its implementation.
