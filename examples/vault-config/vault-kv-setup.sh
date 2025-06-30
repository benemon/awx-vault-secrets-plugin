#!/bin/bash
# Setup Vault KV secrets for static plugin testing

echo "Setting up Vault KV secrets..."

# Enable KV v2 secrets engine
vault secrets enable -path=secret kv-v2

# Store application database credentials
vault kv put secret/myapp/prod/database \
    username="myapp_prod_user" \
    password="super_secure_password_123" \
    host="prod-db.example.com" \
    port="5432" \
    ssl_mode="require"

# Store API keys
vault kv put secret/myapp/prod/apis \
    github_token="ghp_xyz123..." \
    slack_webhook="https://hooks.slack.com/..." \
    sendgrid_api_key="SG.xyz..."

echo "✅ KV secrets setup completed"
