
#!/usr/bin/env bash

# ITIS 3200 — Group 4
# Internal CA Security Testing
# Three-Test Security Demonstration

set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

CA="ca/rootCA.crt"
PASSED=0
FAILED=0

mkdir -p tests/evidence
LOG="tests/evidence/security-demo-$(date +%Y%m%d-%H%M%S).log"

exec > >(tee "$LOG") 2>&1

run_test() {
    local name="$1"
    local expected="$2"
    shift 2

    echo
    echo "========================================"
    echo "$name"
    echo "Expected: $expected"
    echo "========================================"

    local output rc
    output=$("$@" 2>&1)
    rc=$?

    echo "$output"
    echo "Curl exit code: $rc"

    local success=1

    case "$name" in
        "Test 1"*)
            if [[ "$rc" -eq 0 ]] &&
               grep -Eq '^HTTP/[0-9.]+ 200' <<< "$output"; then
                success=0
            fi
            ;;

        "Test 2"*)
            if [[ "$rc" -eq 0 ]] &&
               grep -Eq '^HTTP/[0-9.]+ 200' <<< "$output" &&
               grep -Eiq 'SSL certificate verify ok|SSL certificate verification.*ok' <<< "$output"; then
                success=0
            fi
            ;;

        "Test 3"*)
            if [[ "$rc" -eq 60 ]] &&
               grep -Eiq 'self.signed certificate|certificate verify failed|unknown CA|unable to get local issuer certificate' <<< "$output"; then
                success=0
            fi
            ;;
    esac

    if [[ "$success" -eq 0 ]]; then
        echo "[PASS] $name"
        PASSED=$((PASSED + 1))
    else
        echo "[FAIL] $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "GROUP 4 — INTERNAL CA SECURITY TESTING"

if [[ ! -f "$CA" ]]; then
    echo "ERROR: Root CA certificate not found."
    exit 1
fi

# Test 1 — Fake HTTP Wiki
run_test "Test 1 — Fake HTTP Wiki" \
    "HTTP 200 OK" \
    curl -v -i --max-time 10 --noproxy '*' \
    http://127.0.0.1:8081/

# Test 2 — Legitimate HTTPS Wiki
run_test "Test 2 — Legitimate HTTPS Wiki" \
    "Trusted HTTPS connection succeeds" \
    curl -v -i --max-time 10 --noproxy '*' \
    --resolve wiki.internal.local:8443:127.0.0.1 \
    --cacert "$CA" \
    https://wiki.internal.local:8443/

# Test 3 — Fake HTTPS Wiki
run_test "Test 3 — Fake HTTPS Wiki" \
    "Untrusted certificate rejected (curl 60)" \
    curl -v -i --max-time 10 --noproxy '*' \
    --resolve wiki.internal.local:9443:127.0.0.1 \
    --cacert "$CA" \
    https://wiki.internal.local:9443/

echo
echo "========================================"
echo "FINAL TEST SUMMARY"
echo "========================================"
echo "Passed: $PASSED / 3"
echo "Failed: $FAILED / 3"
echo "Evidence log: $LOG"

if [[ "$FAILED" -eq 0 ]]; then
    echo "ALL THREE SECURITY TESTS PASSED"
    exit 0
else
    echo "ONE OR MORE TESTS FAILED"
    exit 1
fi
