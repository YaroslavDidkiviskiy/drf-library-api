FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN useradd -ms /bin/bash django-user && \
    mkdir -p /app/static && \
    mkdir -p /app/media && \
    chown -R django-user:django-user /app

USER django-user
