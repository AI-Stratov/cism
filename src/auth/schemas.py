from pydantic import BaseModel, Field, constr


class UserRegisterRequest(BaseModel):
    username: str = Field(
        "username", description="Username", example="username",
    )
    password: constr(min_length=8) = Field(
        ..., description="Password", example="mysecretpassword",
    )


class UserRegisterResponse(BaseModel):
    username: str
    message: str


class UserLoginRequest(BaseModel):
    username: str = Field(
        "username", description="Username", example="username",
    )
    password: str = Field(
        ..., description="Password", example="mysecretpassword",
    )


class UserLoginResponse(BaseModel):
    message: str
    token: str


class UserResponse(BaseModel):
    id: int
    username: str
