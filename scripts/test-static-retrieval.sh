#!/bin/bash
# Test static secret retrieval manually

echo "Testing static secret retrieval..."

# Test KV v2 secret
echo "Retrieving password from secret/myapp/prod/database..."
vault kv get -field=password secret/myapp/prod/database

echo "Static secret test completed."
