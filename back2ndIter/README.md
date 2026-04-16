# Сервис проверки стойкости паролей

Веб-приложение для проверки надёжности паролей с оценкой по критериям безопасности и проверкой на наличие в базах утечек.

---

## 🚀 Быстрый старт

### 1. Проверка требований

Убедитесь, что установлен **Python 3.10+**:

```powershell
python --version
```

### 2. Установка зависимостей

```powershell
pip install -r requirements.txt
```

### 3. Запуск сервера

```powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Сервер запустится по адресу: **http://127.0.0.1:8000**

---

## 📁 Структура проекта

```
back2ndIter/
├── backend/
│   ├── main.py                 # Точка входа FastAPI
│   ├── database.py             # Настройки подключения к БД
│   ├── db_depends.py           # Зависимости для DI
│   ├── models/                 # SQLAlchemy модели
│   ├── schemas/                # Pydantic схемы
│   ├── utils/                  # Логика проверки паролей
│   └── migrations/             # Миграции Alembic
├── frontend/
│   ├── index.html              # Главная страница
│   ├── styles.css              # Стили
│   └── script.js               # Клиентская логика
├── tests/                      # Автотесты pytest
├── requirements.txt            # Зависимости Python
└── README.md                   # Эта инструкция
```

---

## 🧪 Тестирование API

### Через браузер

1. Откройте http://127.0.0.1:8000
2. Введите пароль в поле ввода
3. Нажмите «Проверить пароль»
4. Изучите результат в модальном окне

### Через Swagger UI

Откройте http://127.0.0.1:8000/docs и протестируйте эндпоинт `/api/check`

### Через PowerShell

```powershell
$body = @{password = "Test123!"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/check" -Method POST -Body $body -ContentType "application/json"
```
