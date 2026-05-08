# легкий образ Python
FROM python:3.13-slim

# uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# рабочая директорию
WORKDIR /app

# копируем только файлы зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости
RUN uv sync --frozen --no-install-project

# копируем остальной код из корня проекта в /app контейнера
COPY . .

# Финальная синхронизация проекта
RUN uv sync --frozen

# Команда запуска
# --host 0.0.0.0 обязателен для Docker
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]