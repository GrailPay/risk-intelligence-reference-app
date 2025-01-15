import os
from typing import Optional, TypedDict

import requests
from flask import current_app

from app.services.base_service import BaseService
from app.types.verify_response import VerifyResponse


class AccountRoutingService(BaseService):
    def __init__(self, account_number: str, routing_number: str, token: str) -> None:
        self.account_number = account_number
        self.routing_number = routing_number
        self.token = token

    def verify(self) -> Optional[VerifyResponse]:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        payload = {
            "account_number": self.account_number,
            "routing_number": self.routing_number,
        }

        base_url = current_app.config["VERIFY_ACCOUNT_ROUTING_BASE_URL"]
        verify_api_url = f"{base_url}/v1/verify-account-routing"

        try:
            response = self._post(verify_api_url, payload=payload, headers=headers)
            response_data = response.json()

            if response.status_code == 200:
                return VerifyResponse(
                    status=response_data["status"], result=response_data["result"]
                )
            if response.status_code == 400:
                message = "Invalid input data."
                self._log_error(message)
                raise ValueError(message)
            if response.status_code == 401:
                message = "Missing or invalid access token."
                self._log_error(message)
                raise PermissionError(message)
            if response.status_code == 415:
                message = "Unsupported Media Type."
                self._log_error(message)
                raise TypeError(message)
            if response.status_code == 500:
                message = "Internal server error."
                self._log_error(message)
                raise RuntimeError(message)

            response.raise_for_status()
            return None
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None
