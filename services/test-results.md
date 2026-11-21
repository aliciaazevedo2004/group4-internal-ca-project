Member 2 Test Results

Project: Internal Certificate Authority — Group 4
Member 2: Internal Services and HTTPS Configuration
Environment: GitHub Codespace (Linux), certificates generated locally with ca/generate-certs.sh on Nov 21, 2026
Hostnames: wiki.internal.local, api.internal.local (mapped to 127.0.0.1 in /etc/hosts)

Test 1 — HTTP Baseline (Wiki and API)

Purpose: Show that both services run over plain HTTP on separate ports and that a client can load the wiki and retrieve the API response.

Expected Result: The wiki returns its HTML page labeled "HTTP Baseline" on port 8080, and the API /health endpoint returns JSON with "mode":"HTTP" on port 8082.

Actual Result: All four service instances started (wiki on 8080 and 8443, API on 8082 and 8444). curl http://wiki.internal.local:8080/ returned 200 OK with the page text "Welcome to the internal documentation portal (HTTP Baseline)" and the notice that the page is served over plain unencrypted HTTP. curl http://api.internal.local:8082/health returned 200 OK with {"status":"healthy","service":"internal-api","version":"1.0","mode":"HTTP"}.

Status: PASS

Evidence: docs/evidence/member2/3200_FinalProjectM2_HTTPBaseline.png

Test 2 — Certificate Generation and Chain Verification

Purpose: Verify that the wiki and API certificates were issued by the internal Root CA.

Expected Result: openssl verify reports OK for both service certificates against ca/rootCA.crt.

Actual Result: ca/generate-certs.sh completed with "Certificates and keys generated successfully." openssl verify -CAfile ca/rootCA.crt ca/wiki/wiki.crt ca/api/api.crt returned OK for both.

Status: PASS

Evidence: docs/evidence/member2/3200_FinalProjectM2_KeyGeneration.png

Test 3 — Private Key Matches Certificate

Purpose: Confirm that each service uses the private key that belongs to its own certificate, and no other.

Expected Result: The public key hash from each certificate is identical to the public key hash derived from its private key.

Actual Result: Wiki certificate and wiki key both produced SHA-256 8053093f…. API certificate and API key both produced SHA-256 8fe1bdf9…. The wiki and API hashes differ from each other, so each service has its own key pair.

Status: PASS

Evidence: docs/evidence/member2/3200_FinalProjectM2_HashMatches.png

Test 4 — Certificate Subject, SAN, and Validity

Purpose: Verify that each certificate names the correct hostname and is currently valid.

Expected Result: The wiki certificate contains DNS:wiki.internal.local and the API certificate contains DNS:api.internal.local, and both are within their validity period.

Actual Result: ca/wiki/wiki.crt has subject CN=wiki.internal.local and SAN DNS:wiki.internal.local. ca/api/api.crt has subject CN=api.internal.local and SAN DNS:api.internal.local. Both are valid from Nov 21 16:36:51 2026 GMT to Nov 21 16:36:51 2027 GMT.

Status: PASS

Evidence: docs/evidence/member2/3200_FinalProject_Sans_Validity.png

Test 5 — Wiki TLS Verification (HTTPS, Port 8443)

Purpose: Verify that the wiki presents the intended certificate and that the client validates it against the internal Root CA with hostname checking.

Expected Result: The handshake completes with Verification: OK and a verified peer name of wiki.internal.local.

Actual Result: openssl s_client with -CAfile ca/rootCA.crt -verify_hostname wiki.internal.local -verify_return_error returned Verification: OK, Verified peername: wiki.internal.local, and Verify return code: 0 (ok). The chain shows CN=wiki.internal.local issued by CN=Group 4 Internal Root CA. Protocol TLSv1.3, cipher TLS_AES_256_GCM_SHA384, 2048-bit server key.

Status: PASS

Evidence: docs/evidence/member2/3200_FinalProject6.png and docs/evidence/member2/3200_FinalProject6_1.png

Test 6 — API TLS Verification (HTTPS, Port 8444)

Purpose: Verify that the API presents its own certificate, separate from the wiki, and that the client validates it against the internal Root CA.

Expected Result: The handshake completes with Verification: OK and a verified peer name of api.internal.local.

Actual Result: openssl s_client with -CAfile ca/rootCA.crt -verify_hostname api.internal.local -verify_return_error returned Verification: OK, Verified peername: api.internal.local, and Verify return code: 0 (ok). The chain shows CN=api.internal.local issued by CN=Group 4 Internal Root CA. Protocol TLSv1.3, cipher TLS_AES_256_GCM_SHA384, 2048-bit server key.

Status: PASS

Evidence: docs/evidence/member2/3200_FinalProject7.png and docs/evidence/member2/3200_FinalProject7_1.png

Test 7 — HTTPS Application Responses with Explicit CA Trust

Purpose: Verify that a client can load the wiki and retrieve the API response over HTTPS using the real hostnames and --cacert, without disabling verification.

Expected Result: curl --cacert ca/rootCA.crt https://wiki.internal.local:8443/ returns the wiki page labeled "(HTTPS)", and curl --cacert ca/rootCA.crt https://api.internal.local:8444/health returns JSON with "mode":"HTTPS".

Actual Result: curl --cacert ca/rootCA.crt https://wiki.internal.local:8443/ returned 200 OK with the page text "Welcome to the internal documentation portal (HTTPS)" and the notice "This page is served over HTTPS." curl --cacert ca/rootCA.crt https://api.internal.local:8444/health returned 200 OK with the healthy JSON response ("status":"healthy", "service":"internal-api", "version":"1.0"). Both requests succeeded without -k or --insecure. In the screenshot the mode value in the API JSON is partly overwritten by terminal text, so the HTTPS result for the API is shown by the successful TLS request on port 8444 and the Test 6 handshake.

Status: PASS

Evidence: docs/evidence/member2/3200_FinalProjectM2_HTTPSResponses.png

Test 8 — Client Without the Root CA Rejects the Server

Purpose: Show that HTTPS success in Tests 5 to 7 depends on explicit trust of the internal Root CA.

Expected Result: A request without --cacert fails certificate verification.

Actual Result: curl https://wiki.internal.local:8443/ failed with curl: (60) SSL certificate problem: unable to get local issuer certificate. The default trust store does not contain the project's Root CA, so the client refused the connection.

Status: PASS

Evidence: docs/evidence/member2/3200_FinalProject8.png

Summary
Test	Description	Status
1	HTTP baseline (wiki and API)	PASS
2	Certificate chain verification	PASS
3	Private key matches certificate	PASS
4	Subject, SAN, and validity	PASS
5	Wiki TLS verification	PASS
6	API TLS verification	PASS
7	HTTPS application responses with --cacert	PASS
8	Client without Root CA rejects server	PASS