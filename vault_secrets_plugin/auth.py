def authenticate(**kwargs):
    auth_method = kwargs.get("auth_method")
    url = kwargs.get("url").rstrip("/")
    namespace = kwargs.get("namespace")
    headers = {}
    if namespace:
        headers["X-Vault-Namespace"] = namespace

    import requests

    if auth_method == "token":
        return kwargs.get("token"), headers

    elif auth_method == "approle":
        role_id = kwargs.get("role_id")
        secret_id = kwargs.get("secret_id")
        resp = requests.post(f"{url}/v1/auth/approle/login", json={
            "role_id": role_id,
            "secret_id": secret_id
        }, headers=headers)
        resp.raise_for_status()
        token = resp.json()["auth"]["client_token"]
        return token, headers

    elif auth_method == "jwt":
        jwt = kwargs.get("jwt")
        role = kwargs.get("jwt_role")
        resp = requests.post(f"{url}/v1/auth/jwt/login", json={
            "jwt": jwt,
            "role": role
        }, headers=headers)
        resp.raise_for_status()
        token = resp.json()["auth"]["client_token"]
        return token, headers

    else:
        raise ValueError("Unsupported auth_method")