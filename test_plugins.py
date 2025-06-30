"""Test scripts for Vault credential plugins"""

import os
import json
from unittest.mock import patch, MagicMock

def test_vault_static_plugin():
    """Test the static secrets plugin"""
    try:
        from vault_plugins.vault_credentials import vault_static_backend
        
        # Test configuration
        test_config = {
            'url': 'https://vault.example.com:8200',
            'token': 'test-token',
            'mount_point': 'secret',
            'kv_version': 'v2',
            'secret_path': 'myapp/database',
            'secret_key': 'password'
        }
        
        # Mock the requests.get call
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'data': {
                    'username': 'dbuser',
                    'password': 'secret123',
                    'host': 'db.example.com'
                }
            }
        }
        
        with patch('requests.get', return_value=mock_response):
            result = vault_static_backend(**test_config)
            print(f"✓ Static plugin test passed: {result}")
            assert result == 'secret123'
            return True
            
    except Exception as e:
        print(f"✗ Static plugin test failed: {e}")
        return False

def test_vault_dynamic_plugin():
    """Test the dynamic secrets plugin"""
    try:
        from vault_plugins.vault_credentials import vault_dynamic_backend
        
        # Test configuration
        test_config = {
            'url': 'https://vault.example.com:8200',
            'token': 'test-token',
            'mount_point': 'database',
            'role_name': 'readonly',
            'credential_field': 'username'
        }
        
        # Mock the requests.get call
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'username': 'v-approle-readonly-abc123',
                'password': 'dynamic-password-xyz789'
            }
        }
        
        with patch('requests.get', return_value=mock_response):
            result = vault_dynamic_backend(**test_config)
            print(f"✓ Dynamic plugin test passed: {result}")
            assert result == 'v-approle-readonly-abc123'
            return True
            
    except Exception as e:
        print(f"✗ Dynamic plugin test failed: {e}")
        return False

def test_authentication_methods():
    """Test different authentication methods"""
    try:
        from vault_plugins.vault_credentials import vault_auth
        
        # Test token auth
        token_config = {
            'url': 'https://vault.example.com:8200',
            'token': 'test-token'
        }
        
        headers = vault_auth.authenticate(**token_config)
        assert 'X-Vault-Token' in headers
        assert headers['X-Vault-Token'] == 'test-token'
        print("✓ Token authentication test passed")
        
        # Test AppRole auth inference
        approle_config = {
            'url': 'https://vault.example.com:8200',
            'role_id': 'test-role-id',
            'secret_id': 'test-secret-id'
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'auth': {
                'client_token': 'approle-token-123',
                'lease_duration': 3600
            }
        }
        
        with patch('requests.post', return_value=mock_response):
            headers = vault_auth.authenticate(**approle_config)
            assert 'X-Vault-Token' in headers
            print("✓ AppRole authentication test passed")
        
        return True
        
    except Exception as e:
        print(f"✗ Authentication test failed: {e}")
        return False

def run_all_tests():
    """Run all plugin tests"""
    print("🧪 Running Vault credential plugin tests...\n")
    
    tests = [
        ("Authentication Methods", test_authentication_methods),
        ("Static Secrets Plugin", test_vault_static_plugin),
        ("Dynamic Secrets Plugin", test_vault_dynamic_plugin)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print(f"Tests completed: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Plugins are ready for deployment.")
    else:
        print("⚠️  Some tests failed. Review and fix issues before deployment.")

if __name__ == '__main__':
    run_all_tests()
