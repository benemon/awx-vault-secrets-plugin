import requests

def get_aws_secret(kwargs, headers):
    url = kwargs["url"].rstrip("/")
    mount = kwargs["mount"]
    path = kwargs["path"]

    full_url = f"{url}/v1/{mount}/creds/{path}"
    resp = requests.get(full_url, headers=headers)
    resp.raise_for_status()
    data = resp.json()["data"]

    return {
        "aws_access_key": data["access_key"],
        "aws_secret_key": data["secret_key"],
        "aws_session_token": data.get("security_token", "")
    }
