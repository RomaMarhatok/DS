FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml

RUN python -m pip install -U pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install
