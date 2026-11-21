# Certificate Authority Setup

This directory contains the Root CA and certificates used to secure the internal wiki and API.

## Reproducing the Certificates

Private keys are excluded from GitHub. To reproduce the environment, generate a new set of certificates and matching private keys.

From the project root, run:

```bash
bash ca/generate-certs.sh
```

Type `REPLACE` when prompted.

The script generates:

- `ca/rootCA.crt` and `ca/rootCA.key`
- `ca/wiki/wiki.crt` and `ca/wiki/wiki.key`
- `ca/api/api.crt` and `ca/api/api.key`
- `tests/certs/fake-wiki.crt` and `tests/certs/fake-wiki.key`

Existing certificates are replaced locally with new matching certificates and keys.

## Verify Certificates

Run:

```bash
openssl verify -CAfile ca/rootCA.crt ca/wiki/wiki.crt
openssl verify -CAfile ca/rootCA.crt ca/api/api.crt
```

Both should return `OK`.

## Run the Services

Start the wiki:

```bash
python3 -m services.main wiki --mode https
```

Start the API in a separate terminal:

```bash
python3 -m services.main api --mode https
```

See the main `README.md` for security testing instructions.

## Security Notes

- Never upload private keys to GitHub.
- The generated certificates use the existing filenames and paths.
- No Python file changes are required.
- The fake HTTPS certificate is intentionally untrusted.