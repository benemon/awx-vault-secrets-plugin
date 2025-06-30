name = "HashiCorp Vault Static Secret"

inputs = {
    "fields": [
        {"id": "url", "label": "Vault URL", "type": "string"},
        {"id": "namespace", "label": "Vault Namespace", "type": "string"},
        {
            "id": "auth_method",
            "label": "Auth Method",
            "type": "string",
            "choices": [
                {"label": "Token", "value": "token"},
                {"label": "AppRole", "value": "approle"},
                {"label": "JWT", "value": "jwt"}
            ]
        },
        {"id": "token", "label": "Token", "type": "string"},
        {"id": "role_id", "label": "AppRole Role ID", "type": "string"},
        {"id": "secret_id", "label": "AppRole Secret ID", "type": "string"},
        {"id": "jwt", "label": "JWT Token", "type": "string"},
        {"id": "jwt_role", "label": "JWT Role", "type": "string"},
        {
            "id": "kv_version",
            "label": "KV Version",
            "type": "string",
            "default": "2",
            "choices": [
                {"label": "v1", "value": "1"},
                {"label": "v2", "value": "2"}
            ]
        },
        {"id": "mount", "label": "Mount Point", "type": "string"},
        {"id": "path", "label": "Secret Path", "type": "string"},
        {"id": "secret_key", "label": "Secret Key", "type": "string"}
    ],
    "required": ["url", "auth_method", "mount", "path"]
}

injectors = {
    "env": {
        "VAULT_SECRET_JSON": "{{ secret_json }}",
        "VAULT_SECRET_VALUE": "{{ secret_value }}"
    }
}

def backend(**kwargs):
    # For now, return dummy data to confirm wiring
    return {
        "secret_json": '{"dummy":"value"}',
        "secret_value": "dummy_secret"
    }
