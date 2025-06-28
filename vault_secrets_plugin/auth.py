import requests

def authenticate(inputs):
    method = inputs.get("auth_method")

    if method == "token":
        return inputs["token_value"]

    elif method == "approle":
        payload = {
            "role_id": inputs["approle_role_id"],
            "secret_id": inputs["approle_secret_id"]
        }
        mount = inputs.get("approle_mount_point", "approle")
        url = f"{inputs['url']}/v1/auth/{mount}/login"
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()["auth"]["client_token"]

    elif method == "jwt":
        payload = {
            "role": inputs["jwt_role"],
            "jwt": inputs["jwt_token"]
        }
        mount = inputs.get("jwt_mount_point", "jwt")
        url = f"{inputs['url']}/v1/auth/{mount}/login"
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()["auth"]["client_token"]

    else:
        raise ValueError(f"Unsupported auth_method: {method}")
