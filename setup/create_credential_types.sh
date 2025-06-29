#!/usr/bin/env bash
set -euo pipefail

# Edit these before running
AAP_URL="https://your.aap.gateway"
TOKEN="your_bearer_token"

API="$AAP_URL/api/controller/v2"

function create_credential_type() {
  local json_file="../credential_types/$1"
  echo "Uploading $json_file..."
  
  response=$(curl -sS -w "%{http_code}" -o /tmp/response.json -X POST "${API}/credential_types/" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    --data-binary "@${json_file}")

  if [[ "$response" == "201" ]]; then
    echo "✅ Created successfully."
  elif [[ "$response" == "409" ]]; then
    echo "⚠️ Already exists, skipping."
  else
    echo "❌ Error creating credential type. Response:"
    cat /tmp/response.json
    exit 1
  fi
}

create_credential_type "vault_static.json"
create_credential_type "vault_aws.json"
create_credential_type "vault_azure.json"
create_credential_type "vault_db.json"
create_credential_type "vault_auth.json"

echo "Done."
