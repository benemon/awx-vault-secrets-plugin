from setuptools import setup, find_packages

setup(
    name='awx-vault-secrets-plugin',
    version='2.0.0',
    description='HashiCorp Vault Authentication and Secrets Plugins for AWX/AAP',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
        'urllib3>=1.26.0',
    ],
    entry_points={
        'awx.credential_plugins': [
            'vault_auth = vault_plugins:vault_auth_plugin',
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