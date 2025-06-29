#!/usr/bin/env bash
set -euo pipefail

echo "Installing Vault Secrets Plugin into awx-python environment..."
pushd ../
awx-python -m pip install .

echo "Restarting AWX services..."
supervisorctl restart all

echo "Reloading managed plugins after installation..."
awx-manage setup_managed_credential_types
popd
