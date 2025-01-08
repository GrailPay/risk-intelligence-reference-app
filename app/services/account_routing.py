from typing import Optional, TypedDict

import os
import requests


class VerifyResponse(TypedDict):
    status: bool
    result: str


def verify(account_number: str, routing_number: str, token: str) -> Optional[VerifyResponse]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "account_number": account_number,
        "routing_number": routing_number,
    }

    base_url = os.environ.get('VERIFY_ACCOUNT_ROUTING_BASE_URL')
    verify_api_url = f"{base_url}/v1/verify-account-routing"

    try:
        response = requests.post(verify_api_url, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            return VerifyResponse(status=response_data["status"], result=response_data["result"])
        if response.status_code == 400:
            raise ValueError("Invalid input data.")
        if response.status_code == 401:
            raise PermissionError("Missing or invalid access token.")
        if response.status_code == 415:
            raise TypeError("Unsupported Media Type.")
        if response.status_code == 500:
            raise RuntimeError("Internal server error.")

        response.raise_for_status()
        return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
