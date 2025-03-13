from typing import Optional

import requests
from flask import current_app

from app.services.base_service import BaseService
from app.types.verify_ar_v1_response import VerifyARV1Response
from app.types.verify_ar_v2_response import VerifyARV2Response


class AccountRoutingService(BaseService):
    def __init__(self, token: str) -> None:
        self.token = token
        self.base_url = current_app.config["RI_API_BASE_URL"]

    def verify_ar_v1(
        self, account_number: str, routing_number: str
    ) -> Optional[VerifyARV1Response]:
        verify_api_url: str = (
            f"{self.base_url}{current_app.config['RI_VERIFY_ACCOUNT_ROUTING_V1_ENDPOINT']}"
        )

        try:
            response = self._post(
                verify_api_url,
                payload=self._get_payload(
                    account_number=account_number, routing_number=routing_number
                ),
                headers=self._get_headers(),
            )
            return self._handle_response(
                response=response, response_type=VerifyARV1Response
            )
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def verify_ar_v2(
        self, account_number: str, routing_number: str
    ) -> Optional[VerifyARV2Response]:
        verify_ar_v2_api_url: str = (
            f"{self.base_url}{current_app.config['RI_VERIFY_ACCOUNT_ROUTING_V2_ENDPOINT']}"
        )

        try:
            response = self._post(
                verify_ar_v2_api_url,
                payload=self._get_payload(
                    account_number=account_number, routing_number=routing_number
                ),
                headers=self._get_headers(),
            )
            return self._handle_response(
                response=response, response_type=VerifyARV2Response
            )
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

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
