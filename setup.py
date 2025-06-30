from setuptools import setup, find_packages

setup(
    name="awx-vault-secrets-plugin",
    version="0.1.0",
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        "awx.credential_plugins": [
            "hashicorp_vault_static_secret = vault_secrets_plugin.static_plugin"
        ]
    },
    install_requires=[
        "requests"
    ]
)
