#!/bin/bash
# ==============================================================
# Automated test script for AIOps Alerts API
# Author: Mayur's AI Assistant
# ==============================================================

API_KEY="MY_SECURE_API_KEY"
BASE_URL="http://127.0.0.1:8000/alerts"

GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m"

PASS_COUNT=0
FAIL_COUNT=0

run_test() {
    DESCRIPTION=$1
    COMMAND=$2
    EXPECTED_STATUS=$3

    echo -n "TEST: $DESCRIPTION ... "
    STATUS_CODE=$(eval "$COMMAND -o /dev/null -w \"%{http_code}\" -s")

    if [ "$STATUS_CODE" -eq "$EXPECTED_STATUS" ]; then
        echo -e "${GREEN}PASS${NC}"
        ((PASS_COUNT++))
    else
        echo -e "${RED}FAIL${NC} (Expected $EXPECTED_STATUS, got $STATUS_CODE)"
        ((FAIL_COUNT++))
    fi
}

echo "=== Running API Tests ==="

# 1. Valid alert
run_test "Valid alert" \
"curl -X POST \"$BASE_URL\" -H \"Content-Type: application/json\" -H \"X-API-Key: $API_KEY\" -d '{\"identifier\": \"alert1\", \"host\": \"host1\", \"message\": \"CPU usage high\"}'" \
200

# 2. Duplicate identifier
run_test "Duplicate identifier (update)" \
"curl -X POST \"$BASE_URL\" -H \"Content-Type: application/json\" -H \"X-API-Key: $API_KEY\" -d '{\"identifier\": \"alert1\", \"host\": \"host1\", \"message\": \"CPU usage critical\"}'" \
200

# 3. Missing identifier
run_test "Missing identifier" \
"curl -X POST \"$BASE_URL\" -H \"Content-Type: application/json\" -H \"X-API-Key: $API_KEY\" -d '{\"host\": \"host1\", \"message\": \"Memory usage high\"}'" \
400

# 4. Missing host
run_test "Missing host" \
"curl -X POST \"$BASE_URL\" -H \"Content-Type: application/json\" -H \"X-API-Key: $API_KEY\" -d '{\"identifier\": \"alert2\", \"message\": \"Disk space low\"}'" \
400

# 5. Invalid API Key
run_test "Invalid API Key" \
"curl -X POST \"$BASE_URL\" -H \"Content-Type: application/json\" -H \"X-API-Key: WRONG_KEY\" -d '{\"identifier\": \"alert3\", \"host\": \"host2\", \"message\": \"Network latency detected\"}'" \
401

# 6. Rate limit (send 6 alerts quickly)
for i in {1..5}
do
  curl -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d "{\"identifier\": \"storm$i\", \"host\": \"host-storm\", \"message\": \"Storm alert $i\"}" \
  -s -o /dev/null
done
run_test "Rate limit exceeded (6th alert)" \
"curl -X POST \"$BASE_URL\" -H \"Content-Type: application/json\" -H \"X-API-Key: $API_KEY\" -d '{\"identifier\": \"storm6\", \"host\": \"host-storm\", \"message\": \"Storm alert 6\"}'" \
429

# 7. Host suppression threshold
for i in {1..3}
do
  curl -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d "{\"identifier\": \"sup-$i\", \"host\": \"host-suppress\", \"message\": \"Suppression alert $i\"}" \
  -s -o /dev/null
done
run_test "Host suppression (4th alert from same host)" \
"curl -X POST \"$BASE_URL\" -H \"Content-Type: application/json\" -H \"X-API-Key: $API_KEY\" -d '{\"identifier\": \"sup-4\", \"host\": \"host-suppress\", \"message\": \"Suppression alert 4\"}'" \
200

# 8. Suppressed host again within 1 minute
run_test "Host still suppressed" \
"curl -X POST \"$BASE_URL\" -H \"Content-Type: application/json\" -H \"X-API-Key: $API_KEY\" -d '{\"identifier\": \"sup-5\", \"host\": \"host-suppress\", \"message\": \"Suppression check\"}'" \
200

# 9. Invalid JSON
run_test "Invalid JSON" \
"curl -X POST \"$BASE_URL\" -H \"Content-Type: application/json\" -H \"X-API-Key: $API_KEY\" -d '{\"identifier\": \"bad-json\", \"host\": \"host1\", \"message\": \"Missing quote}'" \
400

echo
echo -e "${GREEN}PASS: $PASS_COUNT${NC}  ${RED}FAIL: $FAIL_COUNT${NC}"
