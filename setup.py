from setuptools import setup, find_packages

setup(
    name='vault-secrets-plugin',
    version='0.0.1',
    packages=find_packages(),
    entry_points={
        'awx.credential_plugins': [
            'vault_secrets = vault_secrets_plugin.plugin'
        ]
    },
    install_requires=[
        'requests'
    ],
    zip_safe=False
)
