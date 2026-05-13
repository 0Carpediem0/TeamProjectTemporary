from pydantic import BaseModel, Field


class RequestSchema(BaseModel):
    '''
    Схема входящего запроса для передачи пароля.
    '''
    
    password: str


class ResponseSchema(BaseModel):
    '''
    Схема ответа API с результатом проверки.
    '''
    
    strength: str = Field(pattern='weak|medium|strong') 
    scores: int
    reasons: list[str]
