from python:3.12-slim

WORKDIR /stalker_app

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev

COPY . .
COPY certs/ /stalker_app/certs

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root