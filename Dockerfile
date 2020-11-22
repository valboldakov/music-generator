FROM python:3.6-slim

COPY src/requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

COPY src/ .
ENTRYPOINT ["sh", "./run.sh"]
