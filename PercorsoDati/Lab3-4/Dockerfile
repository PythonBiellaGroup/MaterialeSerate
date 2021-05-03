FROM python:3.8-slim-buster

# Metadata
LABEL name="Streamlit Dashboard"
LABEL maintainer="PythoBiellaGroup"
LABEL version="1.0"

ARG YOUR_ENV=".venv"

ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.0.3 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /server
COPY poetry.lock pyproject.toml /server/

#update pip to avoid problems 
# RUN python3 -m pip instal --upgrade pip

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

#Copy all the project files
COPY . /server

#Streamlit configuration
ENV PYTHONPATH /server

RUN mkdir -p /root/.streamlit

#Set the streamlit environment config
# RUN bash -c 'echo -e "\
#     [general]\n\
#     email = \"\"\n\
#     " > /root/.streamlit/credentials.toml'

# RUN bash -c 'echo -e "\
#     [server]\n\
#     enableCORS = false\n\
#     " > /root/.streamlit/config.toml'

# Copy streamlit production configuration
COPY ./config/config.toml /root/.streamlit/config.toml

# Launch etl and streamlit
RUN ["chmod", "+x", "./scripts/run_etl.sh"]
RUN ["chmod", "+x", "./scripts/run_streamlit.sh"]
RUN ["/bin/bash", "./scripts/run_etl.sh"]
ENTRYPOINT ["/bin/bash", "./scripts/run_streamlit.sh"]
# ENTRYPOINT [ "streamlit","run" ]
# CMD ["python3 ./etl.py","app.py"]
# CMD python3 server.py
