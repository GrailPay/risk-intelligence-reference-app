from typing import Any, Dict, Tuple

from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.services.account_routing_service import AccountRoutingService
from app.services.auth_service import AuthService
from app.validators.verify_ar_request import VerifyARRequest

verify_ar_bp = Blueprint("verify_ar", __name__)


@verify_ar_bp.route("/v1/verify-ar", methods=["POST"])
def verify_ar_v1() -> Any:
    data: Dict[str, Any] = request.get_json(silent=True) or {}
    return _handle_verification_request("verify_ar_v1", data)


@verify_ar_bp.route("/v2/verify-ar", methods=["POST"])
def verify_ar_v2() -> Any:
    data: Dict[str, Any] = request.get_json(silent=True) or {}
    return _handle_verification_request("verify_ar_v2", data)


def _handle_verification_request(
    service_method: str, data: Dict[str, Any]
) -> Tuple[Any, int]:
    try:
        validated_data = VerifyARRequest(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    service = AccountRoutingService()
    result = getattr(service, service_method)(
        account_number=validated_data.account_number,
        routing_number=validated_data.routing_number,
    )

    if result is None:
        return jsonify({"error": "Failed to verify"}), 500

    return jsonify(result), 200
