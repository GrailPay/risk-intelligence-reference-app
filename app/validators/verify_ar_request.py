from pydantic import BaseModel, Field


class VerifyARRequest(BaseModel):
    account_number: str = Field(..., max_length=17, pattern=r"^\d+$")
    routing_number: str = Field(..., min_length=9, max_length=9, pattern=r"^\d+$")
