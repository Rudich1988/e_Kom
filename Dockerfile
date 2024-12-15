FROM python:3.12.5-slim-bullseye

WORKDIR /app

COPY ./src/poetry.lock ./src/pyproject.toml /app/

COPY .env /app/.env

RUN pip install poetry

RUN poetry install --no-dev

COPY ./src /app/src

ENV PYTHONPATH=/app/src

#CMD ["poetry", "run", "uvicorn", "project.app:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]

RUN apt-get update && apt-get install -y netcat

CMD ["sh", "-c", "until nc -z -v -w30 mongodb 27017; do echo 'Waiting for MongoDB...'; sleep 5; done; poetry run uvicorn project.app:app --host 0.0.0.0 --port 8080 --reload"]


