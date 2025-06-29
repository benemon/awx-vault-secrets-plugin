import json
import requests

def get_static_secret(kwargs, headers):
    url = kwargs["url"].rstrip("/")
    mount = kwargs["mount"]
    path = kwargs["path"]
    version = kwargs.get("version")
    secret_key = kwargs.get("secret_key")

    if version:
        full_url = f"{url}/v1/{mount}/data/{path}"
    else:
        full_url = f"{url}/v1/{mount}/{path}"

    resp = requests.get(full_url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    if version:
        secret_data = data["data"]["data"]
    else:
        secret_data = data["data"]

    if secret_key:
        return {"secret_value": secret_data[secret_key]}
    else:
        return {"secret_json": json.dumps(secret_data)}
