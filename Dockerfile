FROM python:3.9-slim-buster

RUN mkdir -p /app/bot/
WORKDIR /app
COPY ./bot /app/bot/
COPY .env alembic.ini Pipfile.lock /app/

RUN pip install -U pip && pip install pipenv
RUN pipenv requirements > requirements.txt
RUN cd /app && pip install -r requirements.txt
