from .auth import authenticate

name = "HashiCorp Vault Dynamic Secret"

metadata = {
    "version": "1.0",
    "author": "Benjamin Holmes",
    "description": "Retrieve dynamic secrets (AWS, Azure, DB) from HashiCorp Vault."
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
        {"id": "engine_type", "label": "Engine Type", "type": "string", "choices": [
            {"label": "AWS", "value": "aws"},
            {"label": "Azure", "value": "azure"},
            {"label": "Database", "value": "database"}
        ]},
        {"id": "mount", "label": "Mount Point", "type": "string"},
        {"id": "role_name", "label": "Role Name", "type": "string"}
    ],
    "required": ["url", "auth_method", "mount", "role_name", "engine_type"]
}

injectors = {
    "env": {
        "AWS_ACCESS_KEY_ID": "{{ aws_access_key }}",
        "AWS_SECRET_ACCESS_KEY": "{{ aws_secret_key }}",
        "AWS_SESSION_TOKEN": "{{ aws_session_token }}",
        "DB_USERNAME": "{{ db_username }}",
        "DB_PASSWORD": "{{ db_password }}",
        "ARM_CLIENT_ID": "{{ arm_client_id }}",
        "ARM_CLIENT_SECRET": "{{ arm_client_secret }}",
        "ARM_TENANT_ID": "{{ arm_tenant_id }}",
        "ARM_SUBSCRIPTION_ID": "{{ arm_subscription_id }}"
    }
}

def backend(**kwargs):
    import requests
    token, headers = authenticate(**kwargs)

    engine = kwargs.get("engine_type")
    mount = kwargs.get("mount")
    role_name = kwargs.get("role_name")
    url = kwargs.get("url").rstrip("/")

    if engine not in ("aws", "azure", "database"):
        raise ValueError(f"Unsupported engine_type: {engine}")

    path = f"{mount}/creds/{role_name}"
    resp = requests.get(
        f"{url}/v1/{path}",
        headers={**headers, "X-Vault-Token": token}
    )
    resp.raise_for_status()
    data = resp.json()["data"]

    if engine == "aws":
        return {
            "aws_access_key": data["access_key"],
            "aws_secret_key": data["secret_key"],
            "aws_session_token": data.get("security_token")
        }
    elif engine == "azure":
        return {
            "arm_client_id": data["client_id"],
            "arm_client_secret": data["client_secret"],
            "arm_tenant_id": data["tenant_id"],
            "arm_subscription_id": data["subscription_id"]
        }
    elif engine == "database":
        return {
            "db_username": data["username"],
            "db_password": data["password"]
        }
