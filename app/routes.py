from typing import Any, Dict

from flask import Blueprint, request, jsonify
from .services.account_routing import verify

main = Blueprint("main", __name__)

@main.route("/verify", methods=["POST"])
def verify_account_routing() -> Any:
    data: Dict[str, Any] = request.get_json(silent=True) or {}
    account_number: str = data.get("account_number", "")
    routing_number: str = data.get("routing_number", "")
    token: str = data.get("token", "")

    if not account_number or not routing_number or not token:
        return jsonify({"error": "Missing required fields"}), 400

    result = verify(account_number, routing_number, token)

    if result is None:
        return jsonify({"error": "Failed to verify"}), 500

    return jsonify(result), 200
