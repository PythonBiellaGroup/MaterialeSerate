FROM python:3.8-slim-buster

# Metadata
LABEL name="Noodle_API"
LABEL maintainer="Moxoff"
LABEL version="1.0"

WORKDIR /server

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY common ./common
COPY importer ./importer
COPY component_creator ./component_creator
COPY kpi ./kpi
COPY settings ./settings
COPY config.py .
COPY server.py .

ENV PYTHONPATH /server

EXPOSE 8000

CMD python3 server.py
