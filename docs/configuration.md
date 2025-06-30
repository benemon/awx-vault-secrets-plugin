# Configuration Guide

## Static Secrets Configuration

### Credential Setup
1. Create "Vault Static Secrets" credential in AWX
2. Configure connection details:
   - URL: Vault server URL
   - Authentication: Token, AppRole, or Certificate
   - Mount Point: KV engine mount (default: secret)
   - KV Version: v1 or v2

### Metadata Configuration
- Secret Path: Path to secret in Vault
- Secret Key: Specific key to retrieve (optional)

## Dynamic Secrets Configuration

### Credential Setup
1. Create "Vault Dynamic Secrets" credential in AWX
2. Configure connection details (same as static)
3. Configure secrets engine:
   - Mount Point: Secrets engine mount
   - TTL: Credential lifetime

### Metadata Configuration
- Role Name: Vault role for generation
- Credential Field: Which field to return
