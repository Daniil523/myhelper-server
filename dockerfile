# Используем официальный образ Python
FROM python:3.12.2-slim-bookworm

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.1.1
RUN pip install --upgrade pip && \
    pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN ls -la && cat pyproject.toml

RUN poetry config virtualenvs.create false --local && \
    poetry install --only main --no-interaction --no-ansi --no-root

COPY . .