FROM python:3.8.12-slim

COPY . /app

RUN pip install -r /app/requirements.txt
WORKDIR /app

EXPOSE 8765

CMD python -u /app/main.py