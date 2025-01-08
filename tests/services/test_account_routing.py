import os
from flask import Flask

from app.services.account_routing import verify

def test_verify(test_app: Flask) -> None:  # pylint: disable=unused-argument
    access_token = os.environ.get("VERIFY_ACCOUNT_ROUTING_ACCESS_TOKEN", "")

    # Check valid response

    response = verify(
        account_number="11101010",
        routing_number="053200983",
        token=access_token
    )

    assert response
    assert response["status"]
    assert response["result"] == "valid"

    # Check invalid response

    response = verify(
        account_number="11101011",
        routing_number="061103852",
        token=access_token
    )

    assert response
    assert response["status"] is False
    assert response["result"] == "invalid"

    # Check not validated response

    response = verify(
        account_number="11101015",
        routing_number="061103852",
        token=access_token
    )

    assert response
    assert response["status"] is False
    assert response["result"] == "not_validated"
