#!/usr/bin/env bash

# Prompt for the AAP Controller URL
read -p "Enter your AAP Controller URL (e.g., https://awx.example.org): " AAP_URL

# Prompt for the OAuth2 token
read -s -p "Enter your OAuth2 Bearer token: " TOKEN
echo

# Check if files exist
if [[ ! -f vault_secrets_auth_credential_type.json ]]; then
  echo "ERROR: vault_secrets_auth_credential_type.json not found!"
  exit 1
fi

if [[ ! -f vault_secrets_lookup_credential_type.json ]]; then
  echo "ERROR: vault_secrets_lookup_credential_type.json not found!"
  exit 1
fi

# Post the Vault Secrets Auth Credential Type
echo "Creating Vault Secrets Auth Credential Type..."
curl -k -s -o /dev/null -w "%{http_code}\n" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -X POST \
  -d @vault_secrets_auth_credential_type.json \
  "$AAP_URL/api/controller/v2/credential_types/"

# Post the Vault Secrets Lookup Credential Type
echo "Creating Vault Secrets Lookup Credential Type..."
curl -k -s -o /dev/null -w "%{http_code}\n" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -X POST \
  -d @vault_secrets_lookup_credential_type.json \
  "$AAP_URL/api/controller/v2/credential_types/"

echo "Done."
