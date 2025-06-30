from setuptools import setup

setup(
    name="awx-vault-secrets-plugin",
    version="0.0.1",
    packages=["vault_secrets_plugin"],
    entry_points={
        "awx.credential_plugins": [
            "hashicorp_vault_static_secret = vault_secrets_plugin.static_plugin",
            "hashicorp_vault_dynamic_secret = vault_secrets_plugin.dynamic_plugin"
        ]
    },
    install_requires=["requests"]
)