from pydantic import BaseModel, Field


class RequestSchema(BaseModel):
    password: str


class ResponseSchema(BaseModel):
    strength: str = Field(pattern='weak|medium|strong')
    scores: int
    reasons: list[str]
