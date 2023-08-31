from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    lastname: str
    email: str

    class ConfigDict:
        from_attributes = True


class UserAuthenticatedResponse(BaseModel):
    id: int
    name: str
    lastname: str
    email: str
    token: str

    class ConfigDict:
        from_attributes = True


class UserRegisterRequest(BaseModel):
    name: str
    email: str
    lastname: str
    password: str


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserJWTPayload(BaseModel):
    id: int
    name: str
    lastname: str
    email: str
