from .auth import authenticate
from .static_backend import get_static_secret
from .dynamic_aws import get_aws_secret
from .dynamic_db import get_db_secret
from .dynamic_azure import get_azure_secret

name = "Vault Secrets Plugin"

inputs = {
    "fields": [],
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
