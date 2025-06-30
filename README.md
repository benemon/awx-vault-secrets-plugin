# HashiCorp Vault Credential Plugins for AWX/AAP

This package provides two credential plugins for AWX/Ansible Automation Platform that integrate with HashiCorp Vault, designed with separation of concerns mirroring the Vault Secrets Operator.

## Quick Start

1. **Install the plugins:**
   ```bash
   python install.py
   ```

2. **Create credential types:**
   ```bash
   python create_credential_types.py
   ```

3. **Test the installation:**
   ```bash
   python test_plugins.py
   ```

## Features

- **Two distinct plugins**: Static secrets and Dynamic credentials
- **Multiple authentication methods**: Token, AppRole, Certificate
- **Vault Enterprise support**: Namespaces, custom CA certificates
- **Comprehensive error handling**: Clear error messages and logging
- **Production ready**: Token caching, SSL/TLS support

## Documentation

See the `docs/` directory for detailed guides:
- [Installation Guide](docs/installation.md)
- [Configuration Guide](docs/configuration.md)
- [Troubleshooting Guide](docs/troubleshooting.md)

## Examples

Check the `examples/` directory for:
- Ansible playbooks
- AWX job templates
- Vault configuration scripts

## License

Apache License 2.0 - see LICENSE file for details.
