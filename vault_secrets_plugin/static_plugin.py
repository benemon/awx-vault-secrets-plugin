name = "HashiCorp Vault Static Secret"


metadata = {
    "version": "0.1.0",
    "author": "Benjamin Holmes"
}

# No fields in the plugin
inputs = {}

injectors = {
    "env": {
        "VAULT_SECRET_JSON": "{{ secret_json }}",
        "VAULT_SECRET_VALUE": "{{ secret_value }}"
    }
}

def backend(**kwargs):
    # Return dummy data for now
    return {
        "secret_json": '{"dummy":"value"}',
        "secret_value": "dummy_secret"
    }