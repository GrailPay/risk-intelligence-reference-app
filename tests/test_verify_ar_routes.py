from unittest.mock import Mock

import pytest
import requests

from app import create_app


EXAMPLE_ACCOUNT = {"account_number": "0000000001", "routing_number": "000000000"}
EXAMPLE_TOKEN = "test-only-token"


# --- Test fixtures ---
@pytest.fixture
def verification_client():
    """Exercise the real request path without credentials or a live API."""
    app = create_app()
    app.config.update(
        TESTING=True,
        RI_API_BASE_URL="https://example.invalid",
        RI_VERIFY_ACCOUNT_ROUTING_V1_ENDPOINT="/upstream/v1/verification",
        RI_VERIFY_ACCOUNT_ROUTING_V2_ENDPOINT="/upstream/v2/verification",
    )
    return app.test_client()


@pytest.fixture
def upstream(monkeypatch):
    """Keep verification tests isolated from the real upstream."""
    post = Mock(side_effect=AssertionError("Unexpected upstream request"))
    monkeypatch.setattr(requests, "post", post)
    return post


# --- End test fixtures ---


@pytest.mark.parametrize(
    ("version", "payload"),
    [
        ("v1", {"status": True, "result": "valid"}),
        ("v2", {"risk_score": 0.64, "confidence_level": "high"}),
    ],
)
def test_verify_route_forwards_bearer_token(
    verification_client, upstream, version, payload, caplog
):
    upstream.side_effect = None
    upstream.return_value = Mock(spec=requests.Response, status_code=200, ok=True)
    upstream.return_value.json.return_value = payload
    with caplog.at_level("INFO"):
        response = verification_client.post(
            f"/{version}/verify-ar",
            json=EXAMPLE_ACCOUNT,
            headers={"Authorization": f"Bearer {EXAMPLE_TOKEN}"},
        )

    assert response.status_code == 200
    assert response.get_json() == payload
    upstream.assert_called_once_with(
        f"https://example.invalid/upstream/{version}/verification",
        json=EXAMPLE_ACCOUNT,
        headers={
            "Authorization": f"Bearer {EXAMPLE_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    assert "Sending POST request" in caplog.text
    for submitted_number in EXAMPLE_ACCOUNT.values():
        assert submitted_number not in caplog.text
    assert EXAMPLE_TOKEN not in caplog.text


@pytest.mark.parametrize("authorization", [None, "Basic dGVzdDp0ZXN0", "Bearer"])
def test_verify_route_requires_bearer_token(
    verification_client, authorization, upstream
):
    headers = {"Authorization": authorization} if authorization is not None else {}
    response = verification_client.post(
        "/v2/verify-ar", json=EXAMPLE_ACCOUNT, headers=headers
    )

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
    upstream.assert_not_called()


def test_verify_route_preserves_account_validation(verification_client, upstream):
    response = verification_client.post(
        "/v1/verify-ar",
        json={"account_number": "invalid", "routing_number": "000000000"},
        headers={"Authorization": f"Bearer {EXAMPLE_TOKEN}"},
    )

    assert response.status_code == 400
    upstream.assert_not_called()
