# Installation Guide

## Prerequisites
- AWX/AAP environment
- HashiCorp Vault server
- Python 3.6+

## Installation Steps

1. **Install the package:**
   ```bash
   python install.py
   ```

2. **Create credential types:**
   ```bash
   python create_credential_types.py
   ```

3. **Test installation:**
   ```bash
   python test_plugins.py
   ```

## Verification
- Check AWX UI for new credential types
- Create test credentials
- Run example playbooks
