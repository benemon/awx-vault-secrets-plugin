import requests

def get_db_secret(kwargs, headers):
    url = kwargs["url"].rstrip("/")
    mount = kwargs["mount"]
    path = kwargs["path"]

    full_url = f"{url}/v1/{mount}/creds/{path}"
    resp = requests.get(full_url, headers=headers)
    resp.raise_for_status()
    data = resp.json()["data"]

    return {
        "db_username": data["username"],
        "db_password": data["password"]
    }
