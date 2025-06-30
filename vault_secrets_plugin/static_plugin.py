name = "HashiCorp Vault Static Secret"

inputs = {
    "fields": [
        {
            "id": "url",
            "label": "Vault URL",
            "type": "string"
        }
    ],
    "required": ["url"]
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
