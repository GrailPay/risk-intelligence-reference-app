from typing import Any, Dict, Tuple

from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.services.auth_service import AuthService
from app.validators.auth_refresh_request import AuthRefreshRequest
from app.validators.auth_request import AuthRequest

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/v1/auth", methods=["POST"])
def auth() -> Any:
    data: Dict[str, Any] = request.get_json(silent=True) or {}
    try:
        validated_data = AuthRequest(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    service = AuthService()
    result = service.authenticate(
        client_id=validated_data.client_id,
        client_secret=validated_data.client_secret,
    )

    if result is None:
        return jsonify({"error": "Failed to verify"}), 500

    return jsonify(result), 200


@auth_bp.route("/v1/auth/refresh", methods=["POST"])
def refresh() -> Any:
    data: Dict[str, Any] = request.get_json(silent=True) or {}
    try:
        validated_data = AuthRefreshRequest(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    service = AuthService()
    result = service.refresh(refresh_token=validated_data.refresh_token)

    if result is None:
        return jsonify({"error": "Failed to verify"}), 500

    return jsonify(result), 200
