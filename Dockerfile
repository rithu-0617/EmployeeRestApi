# ---- Stage 1: Build ----
FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . .

# ---- Stage 2: Production ----
FROM python:3.12-slim AS production

# Security: run as non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY --from=builder /build/app ./app
COPY --from=builder /build/run.py ./run.py
COPY --from=builder /build/wsgi.py ./wsgi.py

# Create data directory and set permissions
RUN mkdir -p /app/data && chown -R appuser:appuser /app

USER appuser

ENV FLASK_ENV=production \
    PORT=5000

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/v1/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "wsgi:app"]
