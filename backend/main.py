from fastapi import FastAPI
from starlette.responses import PlainTextResponse

app = FastAPI(
    title='Сервис проверки стойкости паролей и их присутствия в базах утечек'
)

tags = ['check_password']


@app.get('/', tags=['root'])
async def root():
    return PlainTextResponse(
        'Сервис проверки стойкости паролей и их присутствия в базах утечек'
    )


@app.post('/api/check', tags=tags)
async def check_password():
    """
    Принимает пароль из тела post-запроса и возвращает
    результат проверки пароля: оценка стойкости (Слабый / Средний / Сильный),
    список причин (короткий / только буквы / есть последовательность 123 / популярное слово)
    """
    return {'message': 'Заглушка'}
