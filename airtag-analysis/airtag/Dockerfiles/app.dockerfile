FROM python:3.8

# Metadata
LABEL name="Application Core"
LABEL maintainer="PBG"
LABEL version="0.1"

ARG YOUR_ENV="virtualenv"

ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.8 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Install poetry dependencies
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y libpq-dev gcc curl

# Install project libraries
#ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install poetry - respects $POETRY_VERSION & $POETRY_HOME
#RUN pip install "poetry==$POETRY_VERSION"

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Project Python definition
WORKDIR /admin_app

#Copy all the project files
COPY pyproject.toml .
COPY poetry.lock .
COPY /app ./app
COPY /alembic ./alembic
COPY .env .
COPY launch.sh .
COPY launch_init.sh .
COPY docs ./docs
COPY mkdocs.yml .

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install $(test "$YOUR_ENV" = production) --no-root --no-dev --no-interaction --no-ansi


#Launch the main (if required)
RUN chmod +x launch.sh
CMD ["bash", "launch.sh"]
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:${APP_ENDPOINT_PORT:-8045}", "app.main:app"]