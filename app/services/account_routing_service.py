import os
from typing import Optional, TypedDict

import requests
from flask import current_app

from app.services.base_service import BaseService
from app.types.verify_ar_v1_response import VerifyARV1Response
from app.types.verify_ar_v2_response import VerifyARV2Response


class AccountRoutingService(BaseService):
    def __init__(self, token: str) -> None:
        self.token = token
        self.base_url = current_app.config["VERIFY_ACCOUNT_ROUTING_BASE_URL"]

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _get_payload(self, account_number: str, routing_number: str) -> dict:
        return {
            "account_number": account_number,
            "routing_number": routing_number,
        }

    def verify_ar_v1(
        self, account_number: str, routing_number: str
    ) -> Optional[VerifyARV1Response]:
        verify_api_url: str = f"{self.base_url}/v1/verify-account-routing"

        try:
            response = self._post(
                verify_api_url,
                payload=self._get_payload(
                    account_number=account_number, routing_number=routing_number
                ),
                headers=self._get_headers(),
            )
            return self._handle_response(response, VerifyARV1Response)
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def verify_ar_v2(
        self, account_number: str, routing_number: str
    ) -> Optional[VerifyARV2Response]:
        verify_ar_v2_api_url: str = f"{self.base_url}/v2/verify-account-routing"

        try:
            response = self._post(
                verify_ar_v2_api_url,
                payload=self._get_payload(
                    account_number=account_number, routing_number=routing_number
                ),
                headers=self._get_headers(),
            )
            return self._handle_response(response, VerifyARV2Response)
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def _handle_response(
        self, response: requests.Response, response_type: TypedDict
    ) -> Optional[TypedDict]:
        response_data = response.json()

        if response.status_code == 200:
            return response_type(**response_data)
        if response.status_code == 400:
            message = "Invalid input data."
        elif response.status_code == 401:
            message = "Missing or invalid access token."
        elif response.status_code == 415:
            message = "Unsupported Media Type."
        elif response.status_code == 500:
            message = "Internal server error."
        else:
            response.raise_for_status()
            return None

        self._log_error(message)
        raise ValueError(message)
