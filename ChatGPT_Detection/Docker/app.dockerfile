ARG python_base_version="0-4-0"

FROM python3.9

# Metadata
LABEL name="chatgpt_detection"
LABEL maintainer="PBG"
LABEL version="0.1"

# Project Python definition
WORKDIR /app

#Copy all the project files
COPY pyproject.toml .
COPY poetry.lock .
COPY poetry.toml .

RUN poetry install --no-interaction --no-ansi --only main && \
    rm -rf /root/.cache/pypoetry

COPY /app ./app
COPY launch.sh .

#Launch the main (if required)
RUN chmod +x launch.sh
CMD ["bash", "launch.sh"]
