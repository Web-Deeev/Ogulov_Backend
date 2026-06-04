# 1. Берем Python 3.12 ( slim-версия, чтобы контейнер не весил много)
FROM python:3.12-slim

# 2. Защита, чтобы Питон не оставлял мусорные файлы
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 3. Нужные инструменты для сборки некоторых библиотек
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Копируем список покупок и скачиваем их
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 5. Создаем безопасного пользователя clinic_user, чтобы код не работал от опасного root-админа
RUN useradd -m clinic_user && chown -R clinic_user:clinic_user /app
USER clinic_user

# 6. Копируем весь остальной код бэкенда в коробку
COPY --chown=clinic_user:clinic_user . .

EXPOSE 8000

# 7. Запускаем! Название config.wsgi меняем, если твоя папка называется иначе
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
