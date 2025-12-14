# Dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

WORKDIR /app

# System dependencies cần thiết cho build wheels và các thư viện ML
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    git \
    curl \
    libgomp1 \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy và clean requirements.txt
COPY requirements.txt .

# Clean requirements.txt - loại bỏ local paths và chỉ giữ package names
RUN sed -i 's/ @ file:\/\/.*//g' requirements.txt && \
    sed -i '/^#/d' requirements.txt && \
    sed -i '/^$/d' requirements.txt

# Upgrade pip và install dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt || \
    (echo "Failed packages - trying without strict versions..." && \
    sed -i 's/==.*//' requirements.txt && \
    pip install --no-cache-dir -r requirements.txt)

# Copy source code
COPY . .

# Expose port
EXPOSE 8000

# Run uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]