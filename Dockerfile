# Dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

WORKDIR /app

# System deps (hay cần cho numpy/pandas/sklearn, build wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    git \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 1) Copy requirements trước để tận dụng cache
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# 2) Copy toàn bộ source code
COPY . .

# Mặc định chạy training
# (tương đương: python training/run_experiments.py)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
