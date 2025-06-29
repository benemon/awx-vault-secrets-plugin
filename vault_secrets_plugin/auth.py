import requests

def authenticate(inputs):
    method = inputs.get("auth_method")
    namespace = inputs.get("namespace")

    common_headers = {}
    if namespace:
        common_headers["X-Vault-Namespace"] = namespace

    if method == "token":
        return inputs["token_value"], common_headers

    elif method == "approle":
        payload = {
            "role_id": inputs["approle_role_id"],
            "secret_id": inputs["approle_secret_id"]
        }
        mount = inputs.get("approle_mount_point", "approle")
        url = f"{inputs['url']}/v1/auth/{mount}/login"
        resp = requests.post(url, json=payload, headers=common_headers)
        resp.raise_for_status()
        return resp.json()["auth"]["client_token"], common_headers

    elif method == "jwt":
        payload = {
            "role": inputs["jwt_role"],
            "jwt": inputs["jwt_token"]
        }
        mount = inputs.get("jwt_mount_point", "jwt")
        url = f"{inputs['url']}/v1/auth/{mount}/login"
        resp = requests.post(url, json=payload, headers=common_headers)
        resp.raise_for_status()
        return resp.json()["auth"]["client_token"], common_headers

    else:
        raise ValueError(f"Unsupported auth_method: {method}")
