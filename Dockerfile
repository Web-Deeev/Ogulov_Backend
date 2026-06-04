# 1. Берем чистый Python 3.12
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 2. Ставим системные инструменты
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Копируем требования и устанавливаем их глобально
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn  # 🔥 Насильно доставляем gunicorn в глобальный PATH

# 4. Создаем безопасного пользователя
RUN useradd -m clinic_user && chown -R clinic_user:clinic_user /app
USER clinic_user

# 5. Копируем весь код проекта
COPY --chown=clinic_user:clinic_user . .

EXPOSE 8000

# 6. Запускаем наш мотор! 
# ВНИМАНИЕ: Если твоя папка с файлом wsgi.py называется не config, а ogulov_clinic, 
# то замени "config.wsgi" на "ogulov_clinic.wsgi"
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
