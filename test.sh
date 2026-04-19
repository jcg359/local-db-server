#!/usr/bin/env bash
set -euo pipefail

NODE_PORT=${PORT:-3000}
PYTHON_PORT=${PYTHON_PORT:-8080}
NODE_BASE="http://localhost:$NODE_PORT"
PYTHON_BASE="http://localhost:$PYTHON_PORT"

passed=0
failed=0

run_dataset() {
  local base=$1
  local name=$2
  local label=$3
  response=$(curl -s -o /tmp/ds_body -w "%{http_code}" "$base/datasets/$name")
  body=$(cat /tmp/ds_body)
  if [ "$response" = "200" ]; then
    echo "  PASS  [$label] $name"
    echo "$body"
    passed=$((passed + 1))
  else
    echo "  FAIL  [$label] $name  [$response]"
    echo "$body"
    failed=$((failed + 1))
  fi
}

echo "==> Initializing MySQL via Node (creating UserPrincipal table and inserting random user)..."
init_response=$(curl -s -o /tmp/init_body -w "%{http_code}" -X POST "$NODE_BASE/init-mysql")
init_body=$(cat /tmp/init_body)
if [ "$init_response" = "200" ]; then
  echo "  PASS  /init-mysql"
  echo "$init_body"
else
  echo "  FAIL  /init-mysql  [$init_response]"
  echo "$init_body"
  echo "Aborting: init failed"
  exit 1
fi

echo ""
echo "==> Querying datasets via Node (port $NODE_PORT)..."
run_dataset "$NODE_BASE" giftsdb_users      "node"
run_dataset "$NODE_BASE" holiday_gifts_users "node"

echo ""
echo "==> Querying datasets via Python (port $PYTHON_PORT)..."
run_dataset "$PYTHON_BASE" giftsdb_users "python"

echo ""
echo "$passed passed, $failed failed"
[ "$failed" -eq 0 ]
