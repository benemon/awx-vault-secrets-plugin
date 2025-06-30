#!/bin/bash
# Test dynamic credential generation manually

echo "Testing dynamic credential generation..."

# Generate readonly credentials
echo "Generating readonly credentials:"
vault read database/creds/dba-readonly

echo "Dynamic credential test completed."
