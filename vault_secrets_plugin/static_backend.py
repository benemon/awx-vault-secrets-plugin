import json
import requests

import json
import requests

def get_static_secret(kwargs, headers):
    url = kwargs["url"].rstrip("/")
    mount = kwargs["mount"]
    path = kwargs["path"]
    kv_version = kwargs.get("kv_version", "2")  # Default to KV v2
    secret_key = kwargs.get("secret_key")
    version = kwargs.get("version")

    if kv_version == "2":
        full_url = f"{url}/v1/{mount}/data/{path}"
        params = {}
        if version:
            params["version"] = version
        resp = requests.get(full_url, headers=headers, params=params)
        resp.raise_for_status()
        secret_data = resp.json()["data"]["data"]

    elif kv_version == "1":
        full_url = f"{url}/v1/{mount}/{path}"
        resp = requests.get(full_url, headers=headers)
        resp.raise_for_status()
        secret_data = resp.json()["data"]

    else:
        raise ValueError(f"Unsupported kv_version: {kv_version}")

    if secret_key:
        return {"secret_value": secret_data[secret_key]}
    else:
        return {"secret_json": json.dumps(secret_data)}
