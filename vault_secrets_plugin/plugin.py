import json
import requests
from .auth import authenticate

# Required plugin metadata
name = "Vault Secrets Plugin"

# This defines the lookup credential schema (NOT the auth credential)
inputs = {
    "fields": {
        "engine_type": {
            "type": "string",
            "choices": ["static", "dynamic"],
            "required": True,
            "label": "Engine Type",
            "help_text": "Select static KV or dynamic engine."
        },
        "mount": {
            "type": "string",
            "required": True,
            "label": "Vault Mount Path",
            "help_text": "Mount path (e.g., kv, database)."
        },
        "path": {
            "type": "string",
            "required": True,
            "label": "Secret Path",
            "help_text": "Path to secret or role."
        },
        "version": {
            "type": "string",
            "label": "Version",
            "help_text": "Version for KV v2 (optional)."
        },
        "secret_key": {
            "type": "string",
            "label": "Secret Key",
            "help_text": "Specific key to extract from Vault response."
        },
        "namespace": {
            "type": "string",
            "label": "Vault Namespace",
            "help_text": "Vault Enterprise namespace (optional)."
        }
    },
    "required": ["engine_type", "mount", "path"]
}

# Optionally, you could define injectors (not required)
injectors = {
    "env": {}
}

def backend(**kwargs):
    """
    Main entry point for AWX to resolve secret values.
    """
    token, auth_headers = authenticate(kwargs)

    # Lookup namespace can override auth namespace
    lookup_namespace = kwargs.get("namespace")
    headers = {
        "X-Vault-Token": token
    }
    if lookup_namespace:
        headers["X-Vault-Namespace"] = lookup_namespace
    else:
        headers.update(auth_headers)

    engine_type = kwargs.get("engine_type")
    mount = kwargs.get("mount")
    path = kwargs.get("path")
    secret_key = kwargs.get("secret_key")
    version = kwargs.get("version")

    if engine_type == "static":
        if version:
            # KV v2
            full_path = f"/v1/{mount}/data/{path}"
        else:
            # KV v1
            full_path = f"/v1/{mount}/{path}"

        url = f"{kwargs['url']}{full_path}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # KV v2 nested response
        if "data" in data.get("data", {}):
            result = data["data"]["data"]
        else:
            result = data["data"]

    elif engine_type == "dynamic":
        full_path = f"/v1/{mount}/{path}"
        url = f"{kwargs['url']}{full_path}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()["data"]

    else:
        raise ValueError(f"Unsupported engine_type: {engine_type}")

    if secret_key:
        return {secret_key: result.get(secret_key)}

    return result
