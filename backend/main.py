from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db_depends import get_db
from backend.schemas.response import RequestSchema, ResponseSchema
from backend.utils.check_strength import check_strength

from .database import lifespan

# Создание экземпляра FastAPI-приложения.
app = FastAPI(
    title="Сервис проверки стойкости паролей и их присутствия в базах утечек",
    lifespan=lifespan,
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


@app.get("/", tags=["root"])
async def root():
    """
    GET-эндпоинт для корневого маршрута.
    """

    return FileResponse(frontend_dir / "index.html")


# Регистрация POST-эндпоинта для проверки пароля.
@app.post("/api/check", tags=["check_password"], response_model=ResponseSchema)
async def check_password(request: RequestSchema, db: AsyncSession = Depends(get_db)):
    """
    Принимает пароль из тела post-запроса и возвращает
    результат проверки пароля: оценка стойкости (Слабый / Средний / Сильный),
    список причин (короткий / только буквы / есть последовательность 123)
    """
    return await check_strength(
        db, request.password
    )  # Запуск проверки пароля и возврат результата клиенту.
