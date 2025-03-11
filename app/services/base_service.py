from abc import ABC
from typing import Any, Dict, Optional, TypedDict

import requests
from flask import current_app


class BaseService(ABC):
    def _post(
        self, url: str, payload: Dict[str, Any], headers: Dict[str, str]
    ) -> requests.Response:
        current_app.logger.info(f"Sending POST request to {url} with payload {payload}")
        response = requests.post(url, json=payload, headers=headers)
        return response

    def _log_error(self, message: str) -> None:
        current_app.logger.error(message)

    def _handle_response(
        self, response: requests.Response, response_type: TypedDict
    ) -> Optional[TypedDict]:
        response_data = response.json()

        if response.ok:
            return response_type(**response_data)
        else:
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
            return None
