FROM python:3.11-alpine

WORKDIR /app

COPY ./ ./

RUN pip3 install "poetry==1.6.1"

RUN poetry export -f requirements.txt --output requirements.txt

RUN pip install -r requirements.txt

CMD uvicorn main:create_app --reload --factory --host 0.0.0.0
