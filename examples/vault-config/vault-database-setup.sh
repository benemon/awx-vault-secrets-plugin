#!/bin/bash
# Setup Vault database secrets engine for dynamic plugin testing

echo "Setting up Vault database secrets engine..."

# Enable database secrets engine
vault secrets enable -path=database database

# Configure PostgreSQL connection
vault write database/config/production-db \
    plugin_name="postgresql-database-plugin" \
    connection_url="postgresql://{{username}}:{{password}}@prod-db.example.com:5432/postgres?sslmode=require" \
    allowed_roles="dba-readonly,dba-readwrite,app-user" \
    username="vault_admin" \
    password="vault_admin_password"

# Create readonly role
vault write database/roles/dba-readonly \
    db_name="production-db" \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
                        GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    default_ttl="1h" \
    max_ttl="24h"

echo "✅ Database secrets engine setup completed"
