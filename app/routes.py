from typing import Any, Dict, Tuple

from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from .services.account_routing_service import AccountRoutingService
from .validators.verify_ar_v1_request import VerifyARV1Request

main = Blueprint("main", __name__)


@main.route("/verify/ar-v1", methods=["POST"])
def verify_ar_v1() -> Any:
    data: Dict[str, Any] = request.get_json(silent=True) or {}
    return handle_verification_request("verify_ar_v1", data)


@main.route("/verify/ar-v2", methods=["POST"])
def verify_ar_v2() -> Any:
    data: Dict[str, Any] = request.get_json(silent=True) or {}
    return handle_verification_request("verify_ar_v2", data)


def handle_verification_request(
    service_method: str, data: Dict[str, Any]
) -> Tuple[Any, int]:
    try:
        validated_data = VerifyARV1Request(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    service = AccountRoutingService(validated_data.token)
    result = getattr(service, service_method)(
        account_number=validated_data.account_number,
        routing_number=validated_data.routing_number,
    )

    if result is None:
        return jsonify({"error": "Failed to verify"}), 500

    return jsonify(result), 200
