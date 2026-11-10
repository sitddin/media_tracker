from pydantic import BaseModel, Field


class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1888, le=2100)


class MovieUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    year: int | None = Field(default=None, ge=1888, le=2100)