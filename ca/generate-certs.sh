#!/usr/bin/env bash
set -euo pipefail

# Recreate all certificates and matching private keys for the local ITIS 3200 lab.
# Run from any directory: bash ca/generate-certs.sh
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CA_DIR="$ROOT_DIR/ca"
TEST_CERT_DIR="$ROOT_DIR/tests/certs"

for cmd in openssl mktemp; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "Missing required command: $cmd" >&2; exit 1; }
done

# Never overwrite local keys/certificates without explicit confirmation.
files=(
  "$CA_DIR/rootCA.crt" "$CA_DIR/rootCA.key"
  "$CA_DIR/wiki/wiki.crt" "$CA_DIR/wiki/wiki.key"
  "$CA_DIR/api/api.crt" "$CA_DIR/api/api.key"
  "$TEST_CERT_DIR/fake-wiki.crt" "$TEST_CERT_DIR/fake-wiki.key"
)
existing=()
for file in "${files[@]}"; do
  [[ ! -e "$file" ]] || existing+=("${file#"$ROOT_DIR"/}")
done
if (( ${#existing[@]} > 0 )); then
  echo "These existing files will be replaced:"
  printf '  %s\n' "${existing[@]}"
  echo "This will invalidate the existing certificate/key set for this local checkout."
  read -r -p "Type REPLACE to continue: " confirmation
  [[ "$confirmation" == "REPLACE" ]] || { echo "Cancelled. No files changed."; exit 1; }
fi

# Build everything in a temporary directory first, so OpenSSL errors do not
# leave a partially regenerated certificate set in the project.
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
umask 077
mkdir -p "$tmp/wiki" "$tmp/api" "$tmp/fake"

# Root CA: self-signed, CA:TRUE, keyCertSign/cRLSign.
openssl req -x509 -newkey rsa:3072 -sha256 -nodes -days 3650 \
  -keyout "$tmp/rootCA.key" -out "$tmp/rootCA.crt" \
  -subj '/CN=Group 4 Internal Root CA' \
  -addext 'basicConstraints=critical,CA:TRUE,pathlen:0' \
  -addext 'keyUsage=critical,keyCertSign,cRLSign' \
  >/dev/null 2>&1

create_service_cert() {
  local service="$1" hostname="$2"
  local dir="$tmp/$service"
  openssl req -new -newkey rsa:2048 -nodes -sha256 \
    -keyout "$dir/$service.key" -out "$dir/$service.csr" \
    -subj "/CN=$hostname" >/dev/null 2>&1
  cat > "$dir/$service.ext" <<EXT
[server_cert]
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
subjectAltName=DNS:$hostname
EXT
  openssl x509 -req -in "$dir/$service.csr" \
    -CA "$tmp/rootCA.crt" -CAkey "$tmp/rootCA.key" \
    -CAcreateserial -out "$dir/$service.crt" \
    -days 365 -sha256 -extfile "$dir/$service.ext" \
    -extensions server_cert >/dev/null 2>&1
  openssl verify -CAfile "$tmp/rootCA.crt" "$dir/$service.crt"
  openssl x509 -in "$dir/$service.crt" -noout -checkhost "$hostname" | grep -q 'does match'
}

create_service_cert wiki wiki.internal.local
create_service_cert api api.internal.local

# Deliberately untrusted fake wiki: self-signed leaf certificate, NOT issued by Root CA.
openssl req -x509 -newkey rsa:2048 -nodes -sha256 -days 365 \
  -keyout "$tmp/fake/fake-wiki.key" -out "$tmp/fake/fake-wiki.crt" \
  -subj '/CN=wiki.internal.local' \
  -addext 'basicConstraints=critical,CA:FALSE' \
  -addext 'keyUsage=critical,digitalSignature,keyEncipherment' \
  -addext 'extendedKeyUsage=serverAuth' \
  -addext 'subjectAltName=DNS:wiki.internal.local' >/dev/null 2>&1

mkdir -p "$CA_DIR/wiki" "$CA_DIR/api" "$TEST_CERT_DIR"
install -m 600 "$tmp/rootCA.key" "$CA_DIR/rootCA.key"
install -m 644 "$tmp/rootCA.crt" "$CA_DIR/rootCA.crt"
for service in wiki api; do
  install -m 600 "$tmp/$service/$service.key" "$CA_DIR/$service/$service.key"
  install -m 644 "$tmp/$service/$service.crt" "$CA_DIR/$service/$service.crt"
done
install -m 600 "$tmp/fake/fake-wiki.key" "$TEST_CERT_DIR/fake-wiki.key"
install -m 644 "$tmp/fake/fake-wiki.crt" "$TEST_CERT_DIR/fake-wiki.crt"

echo
echo 'Certificates and keys generated successfully.'
echo 'Root CA: ca/rootCA.crt / ca/rootCA.key'
echo 'Wiki: ca/wiki/wiki.crt / ca/wiki/wiki.key'
echo 'API: ca/api/api.crt / ca/api/api.key'
echo 'Fake wiki: tests/certs/fake-wiki.crt / tests/certs/fake-wiki.key'
echo 'Do not commit any .key files. The new .crt files are local changes.'
