"""
HashiCorp Vault Credential Plugins for AWX

This module provides two credential plugins:
1. vault_static_plugin - For static secrets from KV stores
2. vault_dynamic_plugin - For dynamic credential generation

Usage:
    The plugins are automatically registered via entry_points in setup.py
"""

from .vault_credentials import vault_static_plugin, vault_dynamic_plugin

__version__ = '1.0.0'
__all__ = ['vault_static_plugin', 'vault_dynamic_plugin']
