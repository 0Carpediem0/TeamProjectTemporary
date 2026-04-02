from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import PlainTextResponse

from backend.db_depends import get_db
from backend.schemas.response import ResponseSchema, RequestSchema
from backend.utils.check_strength import check_strength

app = FastAPI(
    title='Сервис проверки стойкости паролей и их присутствия в базах утечек'
)

tags = ['check_password']


@app.get('/', tags=['root'])
async def root():
    return PlainTextResponse(
        'Сервис проверки стойкости паролей и их присутствия в базах утечек'
    )


@app.post('/api/check', tags=tags, response_model=ResponseSchema)
async def check_password(request: RequestSchema, db: AsyncSession = Depends(get_db)):
    """
    Принимает пароль из тела post-запроса и возвращает
    результат проверки пароля: оценка стойкости (Слабый / Средний / Сильный),
    список причин (короткий / только буквы / есть последовательность 123 / популярное слово)
    """
    result = await check_strength(db, request.password)
    return result
