# AWX Vault Secrets Plugin

A custom credential plugin for AWX / AAP that integrates with HashiCorp Vault,
supporting both static and dynamic secrets engines.

## Supported Authentication Methods

- Token
- AppRole
- JWT

## Supported Engine Types

- Static secrets (KV v1/v2)
- Dynamic secrets (e.g., database, AWS, etc.)

## Installation

```bash
pip install -e .
```

## Usage

Register this plugin in AWX using the provided credential type schema and point
your secrets resolution to use `vault_secrets`.
