import requests

def get_azure_secret(kwargs, headers):
    url = kwargs["url"].rstrip("/")
    mount = kwargs["mount"]
    path = kwargs["path"]

    full_url = f"{url}/v1/{mount}/creds/{path}"
    resp = requests.get(full_url, headers=headers)
    resp.raise_for_status()
    data = resp.json()["data"]

    return {
        "arm_client_id": data["client_id"],
        "arm_client_secret": data["client_secret"],
        "arm_tenant_id": data["tenant_id"],
        "arm_subscription_id": data["subscription_id"]
    }
