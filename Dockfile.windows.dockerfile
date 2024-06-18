# Dockerfile for Flask API
FROM python:3.9-slim

WORKDIR /api

COPY api.py .

RUN pip install flask

CMD ["python3", "flask-api.py"]

EXPOSE 5000
