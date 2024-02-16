FROM python:3.11-alpine

WORKDIR /app

COPY ./ ./

RUN pip3 install "poetry==1.6.1"

RUN poetry install

CMD poetry run uvicorn main:create_app --reload --factory --host 0.0.0.0
