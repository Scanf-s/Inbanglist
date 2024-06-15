# Python 3.12와 Alpine Linux 3.20을 기반으로 하는 이미지 사용
FROM python:3.12-alpine3.20

# 이미지의 유지 관리자를 지정
LABEL maintainer="sullungim"

# Python의 표준 입출력 버퍼링을 비활성화하여 로그가 즉시 출력되도록 설정
ENV PYTHONUNBUFFERED=1

# 로컬 파일 시스템의 requirements.txt 파일을 컨테이너로 복사
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app

# 작업 디렉토리를 /app으로 설정
WORKDIR /app

# curl 설치를 위한 추가
RUN apk add --no-cache curl

# DEV 인수를 false로 설정 (기본값)
ARG DEV=false

# 패키지 설치 및 이미지 최적화
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache jpeg-dev zlib zlib-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base musl-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt ; fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# 경로 설정
ENV PATH="/py/bin:$PATH"

# 컨테이너가 8000번 포트를 노출하도록 설정 (Django)
EXPOSE 8000

# django-user로 실행
USER django-user

# Django 프로젝트 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application", "--workers", "4", "--log-level", "debug"]
