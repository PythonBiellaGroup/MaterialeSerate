ARG python_base_version="0-4-0"

FROM gitlab-registry.mdpi.com:8081/ai/libraries/dockbase/python-base:${python_base_version} as python-base

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
