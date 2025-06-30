#!/usr/bin/env bash
set -euo pipefail

echo "Installing Vault Secrets Plugin into awx-python environment..."
pushd ../
awx-python -m pip install .

awx-manage setup_managed_credential_types

echo "Restarting AWX services..."
automation-controller-service restart
popd
