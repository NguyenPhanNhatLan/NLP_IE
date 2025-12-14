
FROM python:3.10-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/root/.cargo/bin:${PATH}"

WORKDIR /app

# Build deps cho Python packages (scipy/sklearn/tokenizers/underthesea/psycopg2...)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ \
    curl pkg-config \
    libssl-dev libffi-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt /app/requirements.txt

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    python -m pip install -U pip setuptools wheel maturin && \
    mkdir -p /wheels && \
    python -m pip wheel --wheel-dir /wheels -r /app/requirements.txt


FROM python:3.10-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir --no-index --find-links=/wheels -r /app/requirements.txt && \
    rm -rf /wheels

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
