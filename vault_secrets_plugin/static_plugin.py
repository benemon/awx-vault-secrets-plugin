name = "HashiCorp Vault Static Secret"


metadata = {
    "version": "0.1.0",
    "author": "Benjamin Holmes"
}

inputs = {
    "fields": [
        {"id": "url", "label": "Vault URL", "type": "string"},
        {"id": "namespace", "label": "Vault Namespace", "type": "string"},
        {"id": "token", "label": "Token", "type": "string"},
        {"id": "role_id", "label": "AppRole Role ID", "type": "string"},
        {"id": "secret_id", "label": "AppRole Secret ID", "type": "string"},
        {"id": "jwt", "label": "JWT Token", "type": "string"},
        {"id": "jwt_role", "label": "JWT Role", "type": "string"},
        {"id": "mount", "label": "Mount Point", "type": "string"},
        {"id": "path", "label": "Secret Path", "type": "string"},
        {"id": "secret_key", "label": "Secret Key", "type": "string"}
    ],
    "required": ["url", "mount", "path"]
}


injectors = {
    "env": {
        "VAULT_SECRET_JSON": "{{ secret_json }}"
    }
}

def backend(**kwargs):
    return {
        "secret_json": '{"dummy":"value"}'
    }
