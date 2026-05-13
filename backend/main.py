from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path

from backend.db_depends import get_db
from backend.schemas.response import ResponseSchema, RequestSchema
from backend.utils.check_strength import check_strength

# Создание экземпляра FastAPI-приложения.
app = FastAPI(
    title='Сервис проверки стойкости паролей и их присутствия в базах утечек'
)

# Подключаем директорию frontend как статическую
frontend_dir = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

# Добавление middleware для обработки CORS-запросов.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
    ],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

tags = ['check_password'] # Создание тега для группировки эндпоинтов в документации.

@app.get('/', tags=['root'])
async def root():
    '''
    GET-эндпоинт для корневого маршрута.
    '''
    
    return FileResponse(frontend_dir / "index.html")

 # Регистрация POST-эндпоинта для проверки пароля.
@app.post('/api/check', tags=tags, response_model=ResponseSchema)
async def check_password(request: RequestSchema, db: AsyncSession = Depends(get_db)):
    """
    Принимает пароль из тела post-запроса и возвращает
    результат проверки пароля: оценка стойкости (Слабый / Средний / Сильный),
    список причин (короткий / только буквы / есть последовательность 123)
    """
    return await check_strength(db, request.password) # Запуск проверки пароля и возврат результата клиенту.
