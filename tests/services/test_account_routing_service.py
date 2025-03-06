import os

from flask import Flask

from app.services.account_routing_service import AccountRoutingService


def test_verify_ar_v1(test_app: Flask) -> None:  # pylint: disable=unused-argument
    access_token = os.getenv("VERIFY_ACCOUNT_ROUTING_ACCESS_TOKEN", "")

    # Check valid response

    service = AccountRoutingService(access_token)
    response = service.verify_ar_v1(
        account_number="11101010", routing_number="053200983"
    )

    assert response
    assert response["status"]
    assert response["result"] == "valid"

    # Check invalid response

    service = AccountRoutingService(access_token)
    response = service.verify_ar_v1(
        account_number="11101011", routing_number="061103852"
    )

    assert response
    assert response["status"] is False
    assert response["result"] == "invalid"

    # Check not validated response

    service = AccountRoutingService(access_token)
    response = service.verify_ar_v1(
        account_number="11101015", routing_number="061103852"
    )

    assert response
    assert response["status"] is False
    assert response["result"] == "not_validated"


def test_verify_ar_v2(test_app: Flask):
    access_token = os.getenv("VERIFY_ACCOUNT_ROUTING_ACCESS_TOKEN", "")

    service = AccountRoutingService(token=access_token)
    response = service.verify_ar_v2(
        account_number="11101010", routing_number="053200983"
    )

    assert response
    assert response["confidence_level"] == "high"
    assert response["risk_score"] == 0.642

    service = AccountRoutingService(access_token)
    response = service.verify_ar_v2(
        account_number="11101011", routing_number="061103852"
    )

    assert response
    assert response["confidence_level"] == "high"
    assert response["risk_score"] == 0.61

    service = AccountRoutingService(access_token)
    response = service.verify_ar_v2(
        account_number="11101015", routing_number="061103852"
    )

    assert response
    assert response["confidence_level"] == "high"
    assert response["risk_score"] == 0.61
