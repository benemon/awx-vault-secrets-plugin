"""Installation helper script for AWX Vault credential plugins"""

import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def install_plugin():
    """Install the plugin package"""
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '.'
        ], check=True, capture_output=True, text=True)
        
        logger.info("Plugin package installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install plugin: {e}")
        return False

def setup_credential_types():
    """Setup credential types in AWX using our custom function"""
    try:
        # Import and run our custom credential type creation
        logger.info("Creating custom Vault credential types...")
        
        # Run the custom creation function
        result = subprocess.run([
            'awx-manage', 'shell', '-c', 
            'exec(open("create_credential_types.py").read())'
        ], check=True, capture_output=True, text=True)
        
        logger.info("Custom credential types created successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to create custom credential types: {e}")
        logger.error(f"Error output: {e.stderr}")
        
        # Fallback to the standard AWX method
        logger.info("Falling back to standard AWX credential type setup...")
        try:
            result = subprocess.run([
                'awx-manage', 'setup_managed_credential_types'
            ], check=True, capture_output=True, text=True)
            
            logger.warning("Standard credential types created, but they will have technical names")
            logger.warning("Run 'python create_credential_types.py' manually for user-friendly names")
            return True
            
        except subprocess.CalledProcessError as e2:
            logger.error(f"Both custom and standard credential type creation failed: {e2}")
            return False
            
    except FileNotFoundError:
        logger.warning("awx-manage not found - manual credential type creation required")
        return False

def create_credential_types_directly():
    """Create credential types directly in Python"""
    try:
        logger.info("Creating credential types directly...")
        
        # Import Django and AWX models
        import os
        import django
        
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'awx.settings.development')
        django.setup()
        
        from awx.main.models.credential import CredentialType
        
        # Clean up existing types
        existing = CredentialType.objects.filter(
            name__in=["Vault Authentication", "Vault Static Secrets", "Vault Dynamic Secrets",
                     "vault_auth", "vault_static_secrets", "vault_dynamic_secrets"]
        )
        if existing.exists():
            logger.info(f"Cleaning up {existing.count()} existing credential types...")
            existing.delete()
        
        # 1. Vault Authentication
        auth_type = CredentialType.objects.create(
            name="Vault Authentication",
            description="HashiCorp Vault authentication credentials",
            kind="external",
            namespace=None,
            inputs={"plugin_name": "vault_auth"},
            injectors={"env": {"VAULT_AUTH_DATA": "{{ auth_data }}"}},
            managed=True
        )
        logger.info(f"✅ Created Vault Authentication credential type (ID: {auth_type.id})")
        
        # 2. Vault Static Secrets
        static_type = CredentialType.objects.create(
            name="Vault Static Secrets",
            description="Retrieve static secrets from HashiCorp Vault KV store",
            kind="external",
            namespace=None,
            inputs={"plugin_name": "vault_static_secrets"},
            injectors={"env": {"VAULT_SECRET": "{{ secret_value }}"}},
            managed=True
        )
        logger.info(f"✅ Created Vault Static Secrets credential type (ID: {static_type.id})")
        
        # 3. Vault Dynamic Secrets
        dynamic_type = CredentialType.objects.create(
            name="Vault Dynamic Secrets",
            description="Generate dynamic secrets from HashiCorp Vault",
            kind="external",
            namespace=None,
            inputs={"plugin_name": "vault_dynamic_secrets"},
            injectors={"env": {"VAULT_CREDENTIAL": "{{ credential_value }}"}},
            managed=True
        )
        logger.info(f"✅ Created Vault Dynamic Secrets credential type (ID: {dynamic_type.id})")
        
        logger.info("🎉 All credential types created with user-friendly names!")
        return True
        
    except Exception as e:
        logger.error(f"Failed to create credential types directly: {e}")
        return False

def restart_automation_controller():
    """Restart the automation controller service"""
    try:
        result = subprocess.run([
            'automation-controller-service', 'restart'
        ], check=True, capture_output=True, text=True)
        
        logger.info("Automation controller service restarted successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to restart automation controller service: {e}")
        logger.error(f"Service restart error: {e.stderr}")
        return False
    except FileNotFoundError:
        logger.warning("automation-controller-service command not found - manual restart required")
        logger.info("Please manually restart AWX services")
        return False

def main():
    """Main installation process"""
    logger.info("Starting Vault credential plugins installation...")
    
    # Step 1: Install plugin package
    if not install_plugin():
        logger.error("Installation failed at package installation step")
        sys.exit(1)
    
    # Step 2: Create credential types with proper names
    credential_types_created = False
    
    # Try our custom creation method first
    if setup_credential_types():
        credential_types_created = True
    else:
        # Try direct creation as fallback
        logger.info("Trying direct credential type creation...")
        if create_credential_types_directly():
            credential_types_created = True
    
    if not credential_types_created:
        logger.error("All credential type creation methods failed")
        logger.error("Manual steps required:")
        logger.error("1. Run: awx-manage shell")
        logger.error("2. Run: exec(open('create_credential_types.py').read())")
        sys.exit(1)
    
    # Step 3: Restart automation controller service
    if not restart_automation_controller():
        logger.warning("Service restart failed - please restart manually")
        logger.info("Manual restart command: automation-controller-service restart")
    
    logger.info("Installation process completed!")
    logger.info("Next steps:")
    logger.info("1. Check AWX UI for new credential types with proper names")
    logger.info("2. Create test credentials")
    logger.info("3. Verify plugins are working with test job templates")

if __name__ == '__main__':
    main()