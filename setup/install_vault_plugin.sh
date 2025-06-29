#!/usr/bin/env bash
set -euo pipefail

echo "Installing Vault Secrets Plugin into awx-python environment..."
pushd ../
awx-python -m pip install .

echo "Restarting AWX services..."
supervisorctl restart all

echo "Checking if plugin was discovered..."
awx-manage list_credential_plugins
popd
