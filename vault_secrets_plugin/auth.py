import requests

def authenticate(inputs):
    print("DEBUG: authenticate() called")
    print(f"DEBUG: inputs = {inputs}")

    method = inputs.get("auth_method")
    namespace = inputs.get("namespace")

    common_headers = {}
    if namespace:
        common_headers["X-Vault-Namespace"] = namespace
        print(f"DEBUG: Using namespace header: {namespace}")

    if method == "token":
        print("DEBUG: Using token authentication")
        return inputs["token_value"], common_headers

    elif method == "approle":
        print("DEBUG: Using AppRole authentication")
        payload = {
            "role_id": inputs["approle_role_id"],
            "secret_id": inputs["approle_secret_id"]
        }
        mount = inputs.get("approle_mount_point", "approle")
        url = f"{inputs['url']}/v1/auth/{mount}/login"
        print(f"DEBUG: AppRole login URL: {url}")
        print(f"DEBUG: AppRole payload: {payload}")
        resp = requests.post(url, json=payload, headers=common_headers)
        resp.raise_for_status()
        token = resp.json()["auth"]["client_token"]
        print("DEBUG: Retrieved AppRole token")
        return token, common_headers

    elif method == "jwt":
        print("DEBUG: Using JWT authentication")
        payload = {
            "role": inputs["jwt_role"],
            "jwt": inputs["jwt_token"]
        }
        mount = inputs.get("jwt_mount_point", "jwt")
        url = f"{inputs['url']}/v1/auth/{mount}/login"
        print(f"DEBUG: JWT login URL: {url}")
        print(f"DEBUG: JWT payload: {payload}")
        resp = requests.post(url, json=payload, headers=common_headers)
        resp.raise_for_status()
        token = resp.json()["auth"]["client_token"]
        print("DEBUG: Retrieved JWT token")
        return token, common_headers

    else:
        raise ValueError(f"Unsupported auth_method: {method}")
