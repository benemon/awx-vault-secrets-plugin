# =============================================================================
# FILE: vault_plugins/__init__.py - FIXED with proper display names
# =============================================================================

import collections
from .vault_credentials import (
    vault_auth_backend, vault_static_backend, vault_dynamic_backend,
    VAULT_AUTH_INPUTS, VAULT_STATIC_INPUTS, VAULT_DYNAMIC_INPUTS
)

CredentialPlugin = collections.namedtuple('CredentialPlugin', ['name', 'inputs', 'backend'])

vault_auth_plugin = CredentialPlugin(
    name='Vault Authentication',
    inputs=VAULT_AUTH_INPUTS,
    backend=vault_auth_backend
)

vault_static_plugin = CredentialPlugin(
    name='Vault Static Secret', 
    inputs=VAULT_STATIC_INPUTS,
    backend=vault_static_backend
)

vault_dynamic_plugin = CredentialPlugin(
    name='Vault Dynamic Secret',
    inputs=VAULT_DYNAMIC_INPUTS,
    backend=vault_dynamic_backend
)

__all__ = ['vault_auth_plugin', 'vault_static_plugin', 'vault_dynamic_plugin']