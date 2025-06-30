import collections
from .vault_credentials import (
    vault_auth_backend, vault_static_backend, vault_dynamic_backend,
    VAULT_AUTH_INPUTS, VAULT_STATIC_INPUTS, VAULT_DYNAMIC_INPUTS
)

CredentialPlugin = collections.namedtuple('CredentialPlugin', ['name', 'inputs', 'backend'])

vault_auth_plugin = CredentialPlugin(
    name='vault_auth',
    inputs=VAULT_AUTH_INPUTS,
    backend=vault_auth_backend
)

vault_static_plugin = CredentialPlugin(
    name='vault_static_secrets',
    inputs=VAULT_STATIC_INPUTS,
    backend=vault_static_backend
)

vault_dynamic_plugin = CredentialPlugin(
    name='vault_dynamic_secrets',
    inputs=VAULT_DYNAMIC_INPUTS,
    backend=vault_dynamic_backend
)

__all__ = ['vault_auth_plugin', 'vault_static_plugin', 'vault_dynamic_plugin']