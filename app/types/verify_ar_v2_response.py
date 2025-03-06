from typing import TypedDict


class VerifyARV2Response(TypedDict):
    confidence_level: str
    risk_score: float
