FROM python:3.11-slim as python-base

LABEL authors="megagran"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.5.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN poetry install

FROM python-base as final

WORKDIR /app
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

COPY ./config/ ./config/
COPY /src/ ./src/
COPY main_short.py ./

# alembic stuff
#COPY ./alembic/ ./alembic/
#COPY alembic.ini ./
#COPY create_db.py ./

EXPOSE 24501

CMD ["python", "main_short.py"]
