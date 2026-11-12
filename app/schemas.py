from pydantic import BaseModel, Field


class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1888, le=2100)


class MovieUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    year: int | None = Field(default=None, ge=1888, le=2100)

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)

class UserResponse(BaseModel):
    id: int
    username: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str