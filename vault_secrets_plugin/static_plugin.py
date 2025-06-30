from .auth import authenticate

name = "HashiCorp Vault Static Secret"

metadata = {
    "version": "0.0.1",
    "author": "Benjamin Holmes",
    "description": "Retrieve static KV secrets (v1/v2) from HashiCorp Vault."
}

inputs = {
    "fields": [
        {"id": "url", "label": "Vault URL", "type": "string"},
        {"id": "namespace", "label": "Vault Namespace", "type": "string"},
        {"id": "auth_method", "label": "Auth Method", "type": "string", "choices": [
            {"label": "Token", "value": "token"},
            {"label": "AppRole", "value": "approle"},
            {"label": "JWT", "value": "jwt"}
        ]},
        {"id": "token", "label": "Token", "type": "string"},
        {"id": "role_id", "label": "AppRole Role ID", "type": "string"},
        {"id": "secret_id", "label": "AppRole Secret ID", "type": "string"},
        {"id": "jwt", "label": "JWT Token", "type": "string"},
        {"id": "jwt_role", "label": "JWT Role", "type": "string"},
        {"id": "kv_version", "label": "KV Version", "type": "string", "default": "2", "choices": [
            {"label": "v1", "value": "1"},
            {"label": "v2", "value": "2"}
        ]},
        {"id": "mount", "label": "Mount Point", "type": "string"},
        {"id": "path", "label": "Secret Path", "type": "string"},
        {"id": "secret_key", "label": "Secret Key", "type": "string"}
    ],
    "required": ["url", "auth_method", "mount", "path"]
}

injectors = {
    "env": {
        "VAULT_SECRET_VALUE": "{{ secret_value }}",
        "VAULT_SECRET_JSON": "{{ secret_data | to_json }}"
    }
}

def backend(**kwargs):
    import requests
    token, headers = authenticate(**kwargs)

    kv_version = kwargs.get("kv_version")
    mount = kwargs.get("mount")
    path = kwargs.get("path")
    secret_key = kwargs.get("secret_key")
    url = kwargs.get("url").rstrip("/")

    if kv_version == "2":
        api_path = f"{mount}/data/{path}"
    else:
        api_path = f"{mount}/{path}"

    resp = requests.get(
        f"{url}/v1/{api_path}",
        headers={**headers, "X-Vault-Token": token}
    )
    resp.raise_for_status()
    data = resp.json()
    content = data["data"]["data"] if kv_version == "2" else data["data"]

    if secret_key:
        return {"secret_value": content.get(secret_key)}
    return {"secret_data": content}
