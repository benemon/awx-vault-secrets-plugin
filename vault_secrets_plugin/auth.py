def authenticate(**kwargs):
    """
    Determine Vault authentication method based on provided fields.
    Fail if no method or multiple methods are configured.
    """

    import requests

    url = kwargs.get("url").rstrip("/")
    namespace = kwargs.get("namespace")
    headers = {}

    if namespace:
        headers["X-Vault-Namespace"] = namespace

    # Detect which auth method is configured
    has_token = bool(kwargs.get("token"))
    has_approle = bool(kwargs.get("role_id") and kwargs.get("secret_id"))
    has_jwt = bool(kwargs.get("jwt"))

    methods = [has_token, has_approle, has_jwt]
    num_methods = sum(methods)

    if num_methods == 0:
        raise ValueError(
            "No authentication method configured. "
            "Provide one of: token, AppRole (role_id + secret_id), or JWT."
        )

    if num_methods > 1:
        raise ValueError(
            "Multiple authentication methods configured. "
            "Provide only one of: token, AppRole, or JWT."
        )

    if has_token:
        return kwargs.get("token"), headers

    if has_approle:
        role_id = kwargs.get("role_id")
        secret_id = kwargs.get("secret_id")
        resp = requests.post(
            f"{url}/v1/auth/approle/login",
            json={
                "role_id": role_id,
                "secret_id": secret_id
            },
            headers=headers
        )
        resp.raise_for_status()
        token = resp.json()["auth"]["client_token"]
        return token, headers

    if has_jwt:
        jwt = kwargs.get("jwt")
        role = kwargs.get("jwt_role")
        resp = requests.post(
            f"{url}/v1/auth/jwt/login",
            json={
                "jwt": jwt,
                "role": role
            },
            headers=headers
        )
        resp.raise_for_status()
        token = resp.json()["auth"]["client_token"]
        return token, headers
