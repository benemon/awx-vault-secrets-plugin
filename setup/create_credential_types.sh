#!/usr/bin/env bash
set -euo pipefail

# Edit these before running
AAP_URL="https://your.aap.gateway"
TOKEN="your_bearer_token"

API="$AAP_URL/api/controller/v2"

function create_credential_type() {
  local json_file="../credential_types/$1"
  echo "Uploading $json_file..."
  curl -sSL -X POST "${API}/credential_types/" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    --data-binary "@${json_file}"
  echo ""
}

create_credential_type "vault_static.json"
create_credential_type "vault_aws.json"
create_credential_type "vault_azure.json"
create_credential_type "vault_db.json"

echo "Done."
