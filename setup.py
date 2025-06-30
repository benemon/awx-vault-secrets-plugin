from setuptools import setup, find_packages

setup(
    name='awx-vault-credential-plugins',
    version='1.0.0',
    description='HashiCorp Vault Static and Dynamic Credential Plugins for AWX/AAP',
    long_description='''
    This package provides two credential plugins for AWX/Ansible Automation Platform:
    
    1. Vault Static Secrets - Retrieves static secrets from Vault KV stores
    2. Vault Dynamic Secrets - Generates dynamic credentials from Vault secrets engines
    
    The plugins are designed with separation of concerns, mirroring the Vault Secrets 
    Operator's VaultStaticSecret and VaultDynamicSecret resources.
    ''',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
        'urllib3>=1.26.0',
    ],
    entry_points={
        'awx.credential_plugins': [
            'vault_static_secrets = vault_plugins:vault_static_plugin',
            'vault_dynamic_secrets = vault_plugins:vault_dynamic_plugin',
        ]
    },
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],
    author='Your Organization',
    author_email='devops@yourorg.com',
    url='https://github.com/yourorg/awx-vault-credential-plugins',
    keywords=['ansible', 'awx', 'hashicorp', 'vault', 'credentials', 'secrets'],
)
