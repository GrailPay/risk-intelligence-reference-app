from typing import TypedDict


class AuthResponse(TypedDict):
    access_token: str
    refresh_token: str
