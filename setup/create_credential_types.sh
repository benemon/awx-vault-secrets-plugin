#!/usr/bin/env bash
set -euo pipefail

# Edit these before running
AAP_URL="https://your.aap.gateway"
TOKEN="your_bearer_token"

API="$AAP_URL/api/controller/v2"

function recreate_credential_type() {
  local json_file="../credential_types/$1"
  
  # Extract the name field from the JSON file
  local name
  name=$(jq -r '.name' "$json_file")

  # URL-encode the name
  local urlencoded_name
  urlencoded_name=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$name")

  echo "Processing Credential Type: $name"

  # Look up existing Credential Type by name
  existing_id=$(curl -sSL -H "Authorization: Bearer ${TOKEN}" \
    "${API}/credential_types/?name=${urlencoded_name}" | jq -r '.results[0].id // empty')

  if [[ -n "$existing_id" ]]; then
    echo "⚠️ Found existing Credential Type with ID $existing_id, deleting..."
    curl -sSL -X DELETE "${API}/credential_types/${existing_id}/" \
      -H "Authorization: Bearer ${TOKEN}"
    echo "✅ Deleted."
  else
    echo "ℹ️ No existing Credential Type found."
  fi

  echo "Creating Credential Type from $json_file..."
  response=$(curl -sS -w "%{http_code}" -o /tmp/response.json -X POST "${API}/credential_types/" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    --data-binary "@${json_file}")

  if [[ "$response" == "201" ]]; then
    echo "✅ Created successfully."
  else
    echo "❌ Error creating credential type. Response:"
    cat /tmp/response.json
    exit 1
  fi
}

recreate_credential_type "vault_static.json"
recreate_credential_type "vault_aws.json"
recreate_credential_type "vault_azure.json"
recreate_credential_type "vault_db.json"
recreate_credential_type "vault_auth.json"

echo "All done."
