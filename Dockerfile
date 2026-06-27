FROM python:3.11-slim

WORKDIR /workspaces/promethium

RUN apt-get update && apt-get install -y sqlite3
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1