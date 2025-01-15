from abc import ABC
from typing import Any, Dict

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
