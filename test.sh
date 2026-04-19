#!/usr/bin/env bash
set -euo pipefail

PORT=${PORT:-3000}
BASE="http://localhost:$PORT"

datasets=(
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
    ((passed++))
  else
    echo "  FAIL  $name  [$response]"
    echo "$body"
    ((failed++))
  fi
done

echo ""
echo "$passed passed, $failed failed"
[ "$failed" -eq 0 ]
