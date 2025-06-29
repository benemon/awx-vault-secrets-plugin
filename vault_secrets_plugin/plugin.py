from .auth import authenticate
from .static_backend import get_static_secret
from .dynamic_aws import get_aws_secret
from .dynamic_db import get_db_secret
from .dynamic_azure import get_azure_secret

name = "Vault Secrets Plugin"

inputs = {
    "fields": [
        {"id": "secret_json", "type": "string", "label": "Secret JSON"},
        {"id": "secret_value", "type": "string", "label": "Secret Value"},
        {"id": "aws_access_key", "type": "string", "label": "AWS Access Key"},
        {"id": "aws_secret_key", "type": "string", "label": "AWS Secret Key"},
        {"id": "aws_session_token", "type": "string", "label": "AWS Session Token"},
        {"id": "db_username", "type": "string", "label": "DB Username"},
        {"id": "db_password", "type": "string", "label": "DB Password"},
        {"id": "arm_client_id", "type": "string", "label": "ARM Client ID"},
        {"id": "arm_client_secret", "type": "string", "label": "ARM Client Secret"},
        {"id": "arm_tenant_id", "type": "string", "label": "ARM Tenant ID"},
        {"id": "arm_subscription_id", "type": "string", "label": "ARM Subscription ID"}
    ],
    "required": []
}

injectors = {
    "env": {}
}

def backend(**kwargs):
    token, auth_headers = authenticate(kwargs)

    lookup_namespace = kwargs.get("namespace")
    headers = {"X-Vault-Token": token}
    if lookup_namespace:
        headers["X-Vault-Namespace"] = lookup_namespace
    else:
        headers.update(auth_headers)

    engine_type = kwargs["engine_type"]

    if engine_type == "static":
        return get_static_secret(kwargs, headers)

    elif engine_type == "dynamic":
        dynamic_engine = kwargs["dynamic_engine"]
        if dynamic_engine == "aws":
            return get_aws_secret(kwargs, headers)
        elif dynamic_engine == "database":
            return get_db_secret(kwargs, headers)
        elif dynamic_engine == "azure":
            return get_azure_secret(kwargs, headers)
        else:
            raise ValueError(f"Unsupported dynamic engine: {dynamic_engine}")

    else:
        raise ValueError(f"Unsupported engine_type: {engine_type}")
