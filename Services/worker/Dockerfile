FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser
USER appuser

WORKDIR /app

# Python deps
COPY worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Worker code
COPY worker/ .

# Shared transcoder package
COPY transcoder/ ./transcoder

CMD ["python", "-m", "celery", "-A", "celery_app", "worker", "--loglevel=info"]
