from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    lastname: str
    email: str


class UserAuthenticatedResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    lastname: str
    email: str
    token: str


class UserRegisterRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: str
    lastname: str
    password: str


class UserLoginRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    password: str


class UserJWTPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    lastname: str
    email: str
