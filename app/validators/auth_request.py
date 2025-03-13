from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    client_id: str = Field(..., max_length=255)
    client_secret: str = Field(..., max_length=255)
