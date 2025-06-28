import json
import requests
from .auth import authenticate

def backend(**kwargs):
    token = authenticate(kwargs)

    headers = {
        'X-Vault-Token': token
    }

    engine_type = kwargs.get("engine_type")
    mount = kwargs.get("mount")
    path = kwargs.get("path")
    secret_key = kwargs.get("secret_key")
    version = kwargs.get("version")
    params = kwargs.get("params")

    if engine_type == "static":
        full_path = f"/v1/{mount}/data/{path}" if version else f"/v1/{mount}/{path}"
        url = f"{kwargs['url']}{full_path}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        result = data["data"]["data"] if "data" in data.get("data", {}) else data["data"]

    elif engine_type == "dynamic":
        full_path = f"/v1/{mount}/{path}"
        url = f"{kwargs['url']}{full_path}"
        if params:
            response = requests.post(url, headers=headers, json=json.loads(params))
        else:
            response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()["data"]

    else:
        raise ValueError(f"Unsupported engine_type: {engine_type}")

    if secret_key:
        return {secret_key: result.get(secret_key)}
    return result
