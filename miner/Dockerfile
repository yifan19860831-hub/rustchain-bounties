# RustChain Miner Docker Image
# Usage: docker run -e WALLET_NAME=mywallet -e NODE_URL=http://node:8545 rustchain-miner

FROM python:3.11-slim

LABEL maintainer="RustChain Community"
LABEL description="RustChain Miner Container"
LABEL version="1.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy miner files
COPY rust_miner/ ./rust_miner/
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV WALLET_NAME=""
ENV NODE_URL="http://localhost:8545"
ENV PYTHONUNBUFFERED=1

# Expose miner port
EXPOSE 8545

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8545/health || exit 1

# Run miner
CMD ["python", "rust_miner/miner.py", "--wallet", "$WALLET_NAME", "--node", "$NODE_URL"]