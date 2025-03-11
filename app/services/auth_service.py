from typing import Any, Dict, Optional

import requests
from flask import current_app

from app.services.base_service import BaseService
from app.types.auth_refresh_response import AuthRefreshResponse
from app.types.auth_response import AuthResponse


class AuthService(BaseService):
    def authenticate(
        self, client_id: str, client_secret: str
    ) -> Optional[Dict[str, Any]]:
        authenticate_api_url: str = (
            f"{current_app.config["RI_API_BASE_URL"]}{current_app.config["RI_AUTH_ENDPOINT"]}"
        )

        try:
            response = self._post(
                authenticate_api_url,
                payload=self._get_payload(
                    client_id=client_id, client_secret=client_secret
                ),
                headers=self._get_headers(),
            )
            return self._handle_response(response=response, response_type=AuthResponse)
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def refresh(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        refresh_api_url: str = (
            f"{current_app.config["RI_API_BASE_URL"]}{current_app.config["RI_AUTH_REFRESH_ENDPOINT"]}"
        )

        try:
            response = self._post(
                refresh_api_url,
                headers=self._get_headers(access_token=refresh_token),
                payload={},
            )
            return self._handle_response(
                response=response, response_type=AuthRefreshResponse
            )
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def _get_headers(self, access_token: str | None = None) -> dict:
        headers: dict = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        return headers

    def _get_payload(self, client_id: str, client_secret: str) -> dict:
        return {
            "client_id": client_id,
            "client_secret": client_secret,
        }
