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
    """Setup credential types in AWX"""
    try:
        result = subprocess.run([
            'awx-manage', 'setup_managed_credential_types'
        ], check=True, capture_output=True, text=True)
        
        logger.info("Credential types setup successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to setup credential types: {e}")
        return False
    except FileNotFoundError:
        logger.warning("awx-manage not found - manual credential type creation required")
        return False

def main():
    """Main installation process"""
    logger.info("Starting Vault credential plugins installation...")
    
    if not install_plugin():
        logger.error("Installation failed at package installation step")
        sys.exit(1)
    
    if not setup_credential_types():
        logger.warning("Credential types setup failed - may need manual creation")
    
    logger.info("Installation process completed!")
    logger.info("Run 'python create_credential_types.py' if automatic setup failed")

if __name__ == '__main__':
    main()
