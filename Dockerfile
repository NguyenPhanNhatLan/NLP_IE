# ===== Builder stage =====
FROM python:3.10-slim AS builder

ENV PIP_NO_CACHE_DIR=1
WORKDIR /wheels

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ git python3-dev libpq-dev libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Build wheels một lần
RUN pip wheel --wheel-dir=/wheels \
    fastapi==0.115.0 uvicorn[standard]==0.30.0 pydantic==2.9.0 python-multipart==0.0.20 python-dotenv==1.2.1 \
    sqlalchemy==2.0.44 alembic==1.17.2 psycopg2-binary==2.9.11 pymongo==4.15.4 \
    numpy==1.26.4 pandas==2.3.3 scikit-learn==1.5.0 scipy==1.13.0 \
    transformers==4.40.0 tokenizers==0.19.0 sentence-transformers==2.7.0 huggingface-hub==0.23.0 \
    underthesea==6.8.0 py-vncorenlp==0.1.4 \
    requests==2.32.3 aiohttp==3.9.5 tqdm==4.66.0 pyyaml==6.0.1 pillow==10.3.0 joblib==1.4.0

# ===== Runtime stage =====
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

WORKDIR /app

# runtime libs (không cần compiler)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
