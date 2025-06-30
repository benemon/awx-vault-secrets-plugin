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
    
    if not install_plugin():
        logger.error("Installation failed at package installation step")
        sys.exit(1)
    
    if not setup_credential_types():
        logger.warning("Credential types setup failed - may need manual creation")
    
    # Restart automation controller service after credential types setup
    if not restart_automation_controller():
        logger.warning("Service restart failed - please restart manually")
        logger.info("Manual restart command: automation-controller-service restart")
    
    logger.info("Installation process completed!")
    logger.info("Next steps:")
    logger.info("1. Check AWX UI for new credential types")
    logger.info("2. Run 'python create_credential_types.py' if automatic setup failed")
    logger.info("3. Verify plugins are working with test credentials")

if __name__ == '__main__':
    main()