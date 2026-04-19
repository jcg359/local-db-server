#!/usr/bin/env bash
set -euo pipefail

PORT=${PORT:-3000}
BASE="http://localhost:$PORT"

echo "==> Initializing MySQL (creating UserPrincipal table and inserting random user)..."
init_response=$(curl -s -o /tmp/init_body -w "%{http_code}" -X POST "$BASE/init-mysql")
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
echo "==> Querying datasets..."

datasets=(
  giftsdb_users
  holiday_gifts_users
)

passed=0
failed=0

for name in "${datasets[@]}"; do
  response=$(curl -s -o /tmp/ds_body -w "%{http_code}" "$BASE/datasets/$name")
  body=$(cat /tmp/ds_body)
  if [ "$response" = "200" ]; then
    echo "  PASS  $name"
    echo "$body"
    passed=$((passed + 1))
  else
    echo "  FAIL  $name  [$response]"
    echo "$body"
    failed=$((failed + 1))
  fi
done

echo ""
echo "$passed passed, $failed failed"
[ "$failed" -eq 0 ]
