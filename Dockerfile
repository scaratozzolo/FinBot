FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y git

WORKDIR /workdir
COPY . /workdir/

RUN uv pip install -r pyproject.toml --system

CMD gunicorn src.app:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080