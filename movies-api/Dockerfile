FROM python:3.12.0b3-alpine AS base
RUN apk add --no-cache gcc musl-dev libpq-dev curl
COPY poetry.lock  /app/
COPY pyproject.toml /app/
WORKDIR /app
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev
COPY ./movies_api /app/movies_api

FROM base AS test
COPY ./tests /app/tests
WORKDIR /app
ENV PYTHONPATH=/app
CMD ["pytest"]

FROM base AS prod
WORKDIR /app/movies_api
EXPOSE 8080
ENV PYTHONPATH=/app
CMD ["gunicorn","--timeout", "3600", "wsgi:app", "-b", "0.0.0.0:8080"]

