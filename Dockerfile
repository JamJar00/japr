FROM python:3.11.3-alpine3.17

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.4.2

RUN pip install "poetry==$POETRY_VERSION" \
  && apk update \
  && apk add git \
  && git config --global --add safe.directory '*'

WORKDIR /japr
COPY . /japr

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

ENTRYPOINT ["poetry", "--quiet", "run", "japr", "/app"]
