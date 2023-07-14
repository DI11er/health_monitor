FROM python:3.7-alpine

ENV PYTHONDONTWRITEBYTECODE 1 && PYTHONUNBUFFERED 1

ADD . /app/
RUN pip install --upgrade pip --no-cache-dir -r /app/requirements.txt
