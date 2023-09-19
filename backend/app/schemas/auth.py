from datetime import datetime

from pydantic import BaseModel


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class GoogleTokenRequest(BaseModel):
    token: str


class GoogleDecodedJWT(BaseModel):
    iss: str
    azp: str
    aud: str
    sub: str
    email: str
    email_verified: bool
    nbf: datetime
    name: str
    picture: str
    given_name: str
    family_name: str
    locale: str
    iat: datetime
    exp: datetime
    jti: str
