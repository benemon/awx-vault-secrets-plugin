from setuptools import setup, find_packages

setup(
    name="vault-secrets-plugin",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "awx.credential_plugins": [
            "hashicorp_vault_static_secret = vault_secrets_plugin.static_plugin"
        ]
    },
    install_requires=[],
)
