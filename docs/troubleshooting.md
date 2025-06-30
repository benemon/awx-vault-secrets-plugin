# Troubleshooting Guide

## Common Issues

### Plugin Not Visible
- Verify installation: `python -c "import vault_plugins"`
- Check credential type creation
- Restart AWX services

### Authentication Failures
- Verify Vault connectivity
- Test credentials manually
- Check Vault policies

### Secret Not Found
- Verify secret path exists
- Check KV version matches
- Ensure mount point is correct

## Debug Scripts
- Run: `bash scripts/troubleshoot-vault-plugins.sh`
- Test: `python test_plugins.py`
