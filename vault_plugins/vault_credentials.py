# =============================================================================
# FILE: vault_plugins/__init__.py
# =============================================================================

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

# =============================================================================
# FILE: vault_plugins/vault_credentials.py
# =============================================================================

import collections
import requests
import json
import logging
from datetime import datetime, timedelta
import threading
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

# =============================================================================
# SHARED COMPONENTS
# =============================================================================

class VaultError(Exception):
    """Base exception for Vault-related errors"""
    pass

class VaultAuthenticationError(VaultError):
    """Authentication failed"""
    pass

class VaultConnectionError(VaultError):
    """Connection issues"""
    pass

class VaultSecretNotFoundError(VaultError):
    """Secret not found"""
    pass

class VaultConfigurationError(VaultError):
    """Configuration validation errors"""
    pass

class VaultAuthenticator:
    """Shared authentication handler for Vault plugins"""
    
    def __init__(self):
        self._token_cache = {}
        self._cache_lock = threading.Lock()
    
    def authenticate(self, **kwargs) -> Dict[str, str]:
        """Authenticate and return headers"""
        auth_method = self._infer_auth_method(**kwargs)
        
        if auth_method == 'token':
            return self._token_auth(**kwargs)
        elif auth_method == 'approle':
            return self._approle_auth(**kwargs)
        elif auth_method == 'cert':
            return self._cert_auth(**kwargs)
        else:
            raise VaultAuthenticationError("No valid authentication method found")
    
    def _infer_auth_method(self, **kwargs) -> str:
        """Infer authentication method from provided credentials"""
        if kwargs.get('token'):
            return 'token'
        elif kwargs.get('role_id') and kwargs.get('secret_id'):
            return 'approle'
        elif kwargs.get('client_cert') and kwargs.get('client_key'):
            return 'cert'
        else:
            raise VaultAuthenticationError(
                "No valid authentication credentials provided. "
                "Provide either: token, role_id+secret_id, or client_cert+client_key"
            )
    
    def _token_auth(self, **kwargs) -> Dict[str, str]:
        """Direct token authentication"""
        token = kwargs.get('token')
        if not token:
            raise VaultAuthenticationError("Token required for token authentication")
        
        return self._build_headers(token, kwargs.get('namespace'))
    
    def _approle_auth(self, **kwargs) -> Dict[str, str]:
        """AppRole authentication with token caching"""
        role_id = kwargs.get('role_id')
        secret_id = kwargs.get('secret_id')
        url = kwargs.get('url')
        
        if not all([role_id, secret_id, url]):
            raise VaultAuthenticationError("role_id, secret_id, and url required for AppRole auth")
        
        # Check cache first
        cached_token = self._get_cached_token(role_id)
        if cached_token:
            return self._build_headers(cached_token, kwargs.get('namespace'))
        
        # Authenticate
        auth_url = f"{url.rstrip('/')}/v1/auth/approle/login"
        auth_data = {'role_id': role_id, 'secret_id': secret_id}
        
        headers = {}
        if kwargs.get('namespace'):
            headers['X-Vault-Namespace'] = kwargs['namespace']
        
        try:
            response = requests.post(
                auth_url,
                json=auth_data,
                headers=headers,
                verify=self._get_ssl_verify(kwargs),
                timeout=30
            )
            response.raise_for_status()
            
            auth_response = response.json()
            client_token = auth_response['auth']['client_token']
            lease_duration = auth_response['auth'].get('lease_duration', 3600)
            
            # Cache token (90% of lease duration for safety)
            self._cache_token(role_id, client_token, lease_duration)
            
            return self._build_headers(client_token, kwargs.get('namespace'))
            
        except requests.exceptions.RequestException as e:
            raise VaultAuthenticationError(f"AppRole authentication failed: {str(e)}")
    
    def _cert_auth(self, **kwargs) -> Dict[str, str]:
        """Certificate-based authentication"""
        client_cert = kwargs.get('client_cert')
        client_key = kwargs.get('client_key')
        url = kwargs.get('url')
        
        if not all([client_cert, client_key, url]):
            raise VaultAuthenticationError("client_cert, client_key, and url required")
        
        auth_url = f"{url.rstrip('/')}/v1/auth/cert/login"
        
        try:
            # Write cert/key to temporary files for requests
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as cert_file:
                cert_file.write(client_cert)
                cert_path = cert_file.name
            
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.key') as key_file:
                key_file.write(client_key)
                key_path = key_file.name
            
            try:
                response = requests.post(
                    auth_url,
                    cert=(cert_path, key_path),
                    verify=self._get_ssl_verify(kwargs),
                    timeout=30
                )
                response.raise_for_status()
                
                auth_response = response.json()
                client_token = auth_response['auth']['client_token']
                
                return self._build_headers(client_token, kwargs.get('namespace'))
                
            finally:
                # Clean up temp files
                os.unlink(cert_path)
                os.unlink(key_path)
            
        except requests.exceptions.RequestException as e:
            raise VaultAuthenticationError(f"Certificate authentication failed: {str(e)}")
    
    def _get_ssl_verify(self, kwargs):
        """Determine SSL verification settings"""
        ca_cert = kwargs.get('ca_cert')
        if ca_cert:
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as ca_file:
                ca_file.write(ca_cert)
                return ca_file.name
        return True
    
    def _build_headers(self, token: str, namespace: Optional[str] = None) -> Dict[str, str]:
        """Build request headers"""
        headers = {
            'X-Vault-Token': token,
            'Content-Type': 'application/json'
        }
        if namespace:
            headers['X-Vault-Namespace'] = namespace
        return headers
    
    def _get_cached_token(self, role_id: str) -> Optional[str]:
        """Get cached token if valid"""
        with self._cache_lock:
            cache_entry = self._token_cache.get(role_id)
            if cache_entry and cache_entry['expires'] > datetime.now():
                return cache_entry['token']
        return None
    
    def _cache_token(self, role_id: str, token: str, lease_duration: int):
        """Cache token with expiration"""
        with self._cache_lock:
            expires = datetime.now() + timedelta(seconds=int(lease_duration * 0.9))
            self._token_cache[role_id] = {
                'token': token,
                'expires': expires
            }

# Global authenticator instance
vault_auth = VaultAuthenticator()

def validate_common_inputs(**kwargs):
    """Validate common inputs for auth plugin"""
    errors = []
    
    if not kwargs.get('url'):
        errors.append("Vault URL is required")
    
    url = kwargs.get('url', '')
    if not url.startswith(('http://', 'https://')):
        errors.append("URL must start with http:// or https://")
    
    # Validate auth credentials
    has_token = bool(kwargs.get('token'))
    has_approle = bool(kwargs.get('role_id') and kwargs.get('secret_id'))
    has_cert = bool(kwargs.get('client_cert') and kwargs.get('client_key'))
    
    auth_methods = sum([has_token, has_approle, has_cert])
    if auth_methods == 0:
        errors.append("At least one authentication method required")
    elif auth_methods > 1:
        errors.append("Only one authentication method should be provided")
    
    if errors:
        raise VaultConfigurationError("; ".join(errors))

# =============================================================================
# VAULT AUTHENTICATION CREDENTIAL TYPE
# =============================================================================

VAULT_AUTH_INPUTS = {
    'fields': [
        {
            'id': 'url',
            'label': 'Vault Server URL',
            'type': 'string',
            'help_text': 'Vault server URL (e.g., https://vault.example.com:8200)'
        },
        {
            'id': 'namespace',
            'label': 'Namespace',
            'type': 'string',
            'help_text': 'Vault namespace (Enterprise feature)'
        },
        {
            'id': 'token',
            'label': 'Vault Token',
            'type': 'string',
            'secret': True,
            'help_text': 'Vault authentication token (leave empty if using other auth)'
        },
        {
            'id': 'role_id',
            'label': 'AppRole Role ID',
            'type': 'string',
            'help_text': 'Role ID for AppRole authentication'
        },
        {
            'id': 'secret_id',
            'label': 'AppRole Secret ID',
            'type': 'string',
            'secret': True,
            'help_text': 'Secret ID for AppRole authentication'
        },
        {
            'id': 'client_cert',
            'label': 'Client Certificate',
            'type': 'string',
            'multiline': True,
            'help_text': 'PEM-encoded client certificate for TLS auth'
        },
        {
            'id': 'client_key',
            'label': 'Client Private Key',
            'type': 'string',
            'secret': True,
            'multiline': True,
            'help_text': 'PEM-encoded private key for client certificate'
        },
        {
            'id': 'ca_cert',
            'label': 'CA Certificate',
            'type': 'string',
            'multiline': True,
            'help_text': 'PEM-encoded CA certificate for SSL verification'
        }
    ],
    'required': ['url']
}

def vault_auth_backend(**kwargs):
    """Backend for Vault authentication credential type"""
    try:
        validate_common_inputs(**kwargs)
        
        # Authenticate and get token
        headers = vault_auth.authenticate(**kwargs)
        vault_token = headers.get('X-Vault-Token')
        
        if not vault_token:
            raise VaultAuthenticationError("Failed to obtain Vault token")
        
        # Return authentication details for consumption by other plugins
        auth_data = {
            'vault_url': kwargs['url'].rstrip('/'),
            'vault_token': vault_token,
            'vault_ca_cert': kwargs.get('ca_cert', ''),
        }
        
        return json.dumps(auth_data)
        
    except VaultError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in vault_auth_backend: {str(e)}")
        raise VaultError(f"Unexpected error: {str(e)}")

# =============================================================================
# VAULT STATIC SECRETS CREDENTIAL TYPE
# =============================================================================

VAULT_STATIC_INPUTS = {
    'fields': [
        {
            'id': 'auth_credential_name',
            'label': 'Vault Auth Credential Name',
            'type': 'string',
            'help_text': 'Name of the Vault Authentication credential to use'
        },
        {
            'id': 'namespace',
            'label': 'Namespace',
            'type': 'string',
            'help_text': 'Vault namespace for secret access'
        },
        {
            'id': 'mount_point',
            'label': 'KV Mount Point',
            'type': 'string',
            'default': 'secret',
            'help_text': 'Mount point for KV secrets engine'
        },
        {
            'id': 'kv_version',
            'label': 'KV Version',
            'type': 'string',
            'default': 'v2',
            'help_text': 'KV secrets engine version (v1 or v2)'
        }
    ],
    'metadata': [
        {
            'id': 'secret_path',
            'label': 'Secret Path',
            'type': 'string',
            'help_text': 'Path to secret in Vault (e.g., myapp/database)'
        },
        {
            'id': 'secret_key',
            'label': 'Secret Key',
            'type': 'string',
            'help_text': 'Key name within the secret to retrieve (optional - returns JSON if empty)'
        }
    ],
    'required': ['auth_credential_name', 'secret_path']
}

def _get_vault_auth_from_credential(auth_credential_name):
    """Get Vault authentication by executing the named auth credential"""
    from awx.main.models.credential import Credential
    
    try:
        # Find the auth credential by name
        auth_credential = Credential.objects.get(
            name=auth_credential_name,
            credential_type__name="Vault Authentication"
        )
        
        # Execute the auth credential to get token
        auth_result = vault_auth_backend(**auth_credential.inputs)
        
        return json.loads(auth_result)
        
    except Credential.DoesNotExist:
        raise VaultConfigurationError(f"Vault Authentication credential '{auth_credential_name}' not found")
    except Exception as e:
        raise VaultConfigurationError(f"Failed to get auth from credential '{auth_credential_name}': {str(e)}")

def vault_static_backend(**kwargs):
    """Backend function for retrieving static secrets from Vault KV store"""
    try:
        # Get auth credential name and execute it
        auth_credential_name = kwargs.get('auth_credential_name')
        if not auth_credential_name:
            raise VaultConfigurationError("auth_credential_name is required")
        
        vault_auth_data = _get_vault_auth_from_credential(auth_credential_name)
        
        secret_path = kwargs.get('secret_path')
        if not secret_path:
            raise VaultConfigurationError("secret_path is required for static secrets")
        
        # Extract parameters
        url = vault_auth_data['vault_url']
        vault_token = vault_auth_data['vault_token']
        mount_point = kwargs.get('mount_point', 'secret')
        kv_version = kwargs.get('kv_version', 'v2')
        secret_key = kwargs.get('secret_key')
        namespace = kwargs.get('namespace')
        
        # Build headers
        headers = {
            'X-Vault-Token': vault_token,
            'Content-Type': 'application/json'
        }
        if namespace:
            headers['X-Vault-Namespace'] = namespace
        
        # Build secret URL based on KV version
        if kv_version == 'v1':
            secret_url = f"{url}/v1/{mount_point}/{secret_path}"
        else:  # v2
            secret_url = f"{url}/v1/{mount_point}/data/{secret_path}"
        
        # Retrieve secret
        logger.debug(f"Retrieving static secret from: {secret_url}")
        
        # Use CA cert if provided
        verify_ssl = True
        ca_cert = vault_auth_data.get('vault_ca_cert')
        if ca_cert:
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as ca_file:
                ca_file.write(ca_cert)
                verify_ssl = ca_file.name
        
        response = requests.get(
            secret_url,
            headers=headers,
            verify=verify_ssl,
            timeout=30
        )
        
        # Handle errors
        if response.status_code == 404:
            raise VaultSecretNotFoundError(f"Static secret not found: {secret_path}")
        elif response.status_code == 403:
            raise VaultAuthenticationError("Access denied - check Vault policies")
        elif response.status_code >= 400:
            raise VaultConnectionError(f"Vault API error {response.status_code}: {response.text}")
        
        # Parse response
        response_data = response.json()
        
        # Extract secret data based on KV version
        if kv_version == 'v1':
            secret_data = response_data.get('data', {})
        else:  # v2
            secret_data = response_data.get('data', {}).get('data', {})
        
        # Return specific key or entire secret
        if secret_key:
            if secret_key not in secret_data:
                raise VaultSecretNotFoundError(f"Key '{secret_key}' not found in secret")
            return secret_data[secret_key]
        else:
            # Return entire secret as JSON
            return json.dumps(secret_data)
            
    except VaultError:
        raise
    except requests.exceptions.Timeout:
        raise VaultConnectionError("Vault request timed out")
    except requests.exceptions.ConnectionError as e:
        raise VaultConnectionError(f"Cannot connect to Vault: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in vault_static_backend: {str(e)}")
        raise VaultError(f"Unexpected error: {str(e)}")

# =============================================================================
# VAULT DYNAMIC SECRETS CREDENTIAL TYPE
# =============================================================================

VAULT_DYNAMIC_INPUTS = {
    'fields': [
        {
            'id': 'auth_credential_name',
            'label': 'Vault Auth Credential Name',
            'type': 'string',
            'help_text': 'Name of the Vault Authentication credential to use'
        },
        {
            'id': 'namespace',
            'label': 'Namespace',
            'type': 'string',
            'help_text': 'Vault namespace for secret access'
        },
        {
            'id': 'mount_point',
            'label': 'Secrets Engine Mount',
            'type': 'string',
            'default': 'database',
            'help_text': 'Mount point for dynamic secrets engine'
        },
        {
            'id': 'ttl',
            'label': 'TTL',
            'type': 'string',
            'help_text': 'Time-to-live for dynamic secret (e.g., 1h, 30m)'
        }
    ],
    'metadata': [
        {
            'id': 'role_name',
            'label': 'Role Name',
            'type': 'string',
            'help_text': 'Vault role name for dynamic secret generation'
        },
        {
            'id': 'credential_field',
            'label': 'Credential Field',
            'type': 'string',
            'default': 'username',
            'help_text': 'Which credential field to return (username, password, or full_json)'
        }
    ],
    'required': ['auth_credential_name', 'role_name']
}

def vault_dynamic_backend(**kwargs):
    """Backend function for generating dynamic secrets from Vault"""
    try:
        # Get auth credential name and execute it
        auth_credential_name = kwargs.get('auth_credential_name')
        if not auth_credential_name:
            raise VaultConfigurationError("auth_credential_name is required")
        
        vault_auth_data = _get_vault_auth_from_credential(auth_credential_name)
        
        role_name = kwargs.get('role_name')
        if not role_name:
            raise VaultConfigurationError("role_name is required for dynamic secrets")
        
        # Extract parameters
        url = vault_auth_data['vault_url']
        vault_token = vault_auth_data['vault_token']
        mount_point = kwargs.get('mount_point', 'database')
        credential_field = kwargs.get('credential_field', 'username')
        ttl = kwargs.get('ttl')
        namespace = kwargs.get('namespace')
        
        # Build headers
        headers = {
            'X-Vault-Token': vault_token,
            'Content-Type': 'application/json'
        }
        if namespace:
            headers['X-Vault-Namespace'] = namespace
        
        # Build credentials generation URL
        creds_url = f"{url}/v1/{mount_point}/creds/{role_name}"
        
        # Prepare request data
        request_data = {}
        if ttl:
            request_data['ttl'] = ttl
        
        # Generate dynamic credentials
        logger.debug(f"Generating dynamic credentials from: {creds_url}")
        
        # Use CA cert if provided
        verify_ssl = True
        ca_cert = vault_auth_data.get('vault_ca_cert')
        if ca_cert:
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as ca_file:
                ca_file.write(ca_cert)
                verify_ssl = ca_file.name
        
        if request_data:
            response = requests.post(
                creds_url,
                json=request_data,
                headers=headers,
                verify=verify_ssl,
                timeout=30
            )
        else:
            response = requests.get(
                creds_url,
                headers=headers,
                verify=verify_ssl,
                timeout=30
            )
        
        # Handle errors
        if response.status_code == 404:
            raise VaultSecretNotFoundError(f"Dynamic secret role not found: {role_name}")
        elif response.status_code == 403:
            raise VaultAuthenticationError("Access denied - check Vault policies")
        elif response.status_code >= 400:
            raise VaultConnectionError(f"Vault API error {response.status_code}: {response.text}")
        
        # Parse response
        response_data = response.json()
        credential_data = response_data.get('data', {})
        
        # Return requested credential field
        if credential_field == 'full_json':
            return json.dumps(credential_data)
        elif credential_field in credential_data:
            return credential_data[credential_field]
        else:
            available_fields = list(credential_data.keys())
            raise VaultSecretNotFoundError(
                f"Field '{credential_field}' not found. Available fields: {available_fields}"
            )
            
    except VaultError:
        raise
    except requests.exceptions.Timeout:
        raise VaultConnectionError("Vault request timed out")
    except requests.exceptions.ConnectionError as e:
        raise VaultConnectionError(f"Cannot connect to Vault: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in vault_dynamic_backend: {str(e)}")
        raise VaultError(f"Unexpected error: {str(e)}")