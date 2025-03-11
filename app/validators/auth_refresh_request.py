from pydantic import BaseModel, Field


class AuthRefreshRequest(BaseModel):
    refresh_token: str = Field(...)
