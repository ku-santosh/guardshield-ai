# ==============================================================================
# STAGE 1: Build & Dependency Resolution Compiler
# ==============================================================================
FROM python:3.11-slim AS builder

WORKDIR /build

# Install basic compiler tools required for specific C-extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies into a localized wheel folder layout
RUN pip install --no-cache-dir --user -r requirements.txt

# ==============================================================================
# STAGE 2: Ultra-Lean Production Container Environment
# ==============================================================================
FROM python:3.11-slim AS runner

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed dependencies from the builder stage
COPY --from=builder /root/.local /root/.local
COPY ./app ./app

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Expose API traffic service ports
EXPOSE 8000

# Enforce a non-privileged system user executing the runtime context process
USER 10001

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]