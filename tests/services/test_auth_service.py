import pytest
from flask import Flask

from app.services.auth_service import AuthService


def test_authenticate_success(ri_access_token: str) -> None:
    assert ri_access_token is not None


def test_authenticate_failure(test_app: Flask) -> None:
    auth_service = AuthService()
    auth_response = auth_service.authenticate(
        client_id="invalid_client_id",
        client_secret="invalid_client_secret",
    )

    assert auth_response is None
