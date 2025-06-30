#!/bin/bash
# Comprehensive troubleshooting script

echo "=== Vault Credential Plugins Troubleshooting ==="
echo

# Check plugin installation
echo "1. Checking plugin installation..."
python -c "
try:
    import vault_plugins
    print('✓ Plugin module imported successfully')
    print(f'  Version: {vault_plugins.__version__}')
except ImportError as e:
    print(f'✗ Plugin import failed: {e}')
"

echo

# Check Vault connectivity
echo "2. Checking Vault connectivity..."
vault_url="${VAULT_ADDR:-https://vault.example.com:8200}"
curl -s --connect-timeout 5 "${vault_url}/v1/sys/health" > /dev/null
if [ $? -eq 0 ]; then
    echo "✓ Vault server is reachable"
else
    echo "✗ Cannot connect to Vault server"
fi

echo
echo "=== Troubleshooting completed ==="
