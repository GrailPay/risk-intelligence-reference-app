from typing import Generator

import pytest
from flask import Flask

from app import create_app
from app.services.auth_service import AuthService


@pytest.fixture
def test_app() -> Generator:
    app = create_app()

    with app.app_context():
        yield app


@pytest.fixture
def ri_access_token(test_app: Flask) -> str:
    auth_service = AuthService()
    auth_response = auth_service.authenticate(
        client_id=test_app.config["RI_TEST_CLIENT_ID"],
        client_secret=test_app.config["RI_TEST_CLIENT_SECRET"],
    )

    if auth_response is None:
        pytest.fail("Authentication failed, auth_response is None")

    return auth_response["access_token"]
