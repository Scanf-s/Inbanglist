FROM python:3.12-slim

LABEL maintainer="rbwo"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon-x11-0 \
    libxcomposite1 \
    libxcursor1 \
    libxi6 \
    libxtst6 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    postgresql-client \
    gcc \
    g++ \
    build-essential \
    libpq-dev \
    cron \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    pip install playwright==1.44.0 && \
    playwright install --with-deps

COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab && \
    crontab /etc/cron.d/crontab

CMD ["cron", "-f"]