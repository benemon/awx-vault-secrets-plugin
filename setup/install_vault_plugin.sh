#!/usr/bin/env bash
set -euo pipefail

echo "Installing Vault Secrets Plugin into awx-python environment..."
pushd ../
awx-python -m pip install .

echo "Restarting AWX services..."
automation-controller-service restart
popd
