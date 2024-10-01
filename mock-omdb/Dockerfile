FROM python:3.12.0b3-alpine 
RUN apk add --no-cache gcc musl-dev libpq-dev
COPY poetry.lock  /app/
COPY pyproject.toml /app/
WORKDIR /app
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev
COPY ./mock_omdb /app/mock_omdb

WORKDIR /app/mock_omdb
EXPOSE 8080
CMD ["gunicorn","--timeout", "3600", "--chdir","/app/mock_omdb" ,"app:app", "-b", "0.0.0.0:8080"]
