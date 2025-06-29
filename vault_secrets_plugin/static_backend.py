import json
import requests

def get_static_secret(kwargs, headers):
    print("DEBUG: get_static_secret() called")
    print(f"DEBUG: kwargs = {kwargs}")
    print(f"DEBUG: headers = {headers}")

    url = kwargs["url"].rstrip("/")
    mount = kwargs["mount"]
    path = kwargs["path"]
    kv_version = kwargs.get("kv_version", "2")  # Default to KV v2
    secret_key = kwargs.get("secret_key")
    version = kwargs.get("version")

    if kv_version == "2":
        print("DEBUG: Using KV v2 engine")
        full_url = f"{url}/v1/{mount}/data/{path}"
        params = {}
        if version:
            params["version"] = version
            print(f"DEBUG: Specified secret version: {version}")
        print(f"DEBUG: KV v2 URL: {full_url}")
        resp = requests.get(full_url, headers=headers, params=params)
        resp.raise_for_status()
        secret_data = resp.json()["data"]["data"]
        print(f"DEBUG: Retrieved KV v2 data: {secret_data}")

    elif kv_version == "1":
        print("DEBUG: Using KV v1 engine")
        full_url = f"{url}/v1/{mount}/{path}"
        print(f"DEBUG: KV v1 URL: {full_url}")
        resp = requests.get(full_url, headers=headers)
        resp.raise_for_status()
        secret_data = resp.json()["data"]
        print(f"DEBUG: Retrieved KV v1 data: {secret_data}")

    else:
        raise ValueError(f"Unsupported kv_version: {kv_version}")

    if secret_key:
        value = secret_data[secret_key]
        print(f"DEBUG: Returning single secret key '{secret_key}': {value}")
        return {"secret_value": value}
    else:
        serialized = json.dumps(secret_data)
        print(f"DEBUG: Returning full secret JSON")
        return {"secret_json": serialized}
