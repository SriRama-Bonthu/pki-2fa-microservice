# ========================
# Stage 1: Builder
# ========================
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Copy dependency file and install (for caching)
COPY requirements.txt .

# Install Python dependencies into a separate folder /install
RUN pip install --prefix=/install -r requirements.txt


# ========================
# Stage 2: Runtime
# ========================
FROM python:3.11-slim

# Avoid interactive prompts and set timezone env
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Set working directory inside container
WORKDIR /app

# Install system dependencies: cron + timezone data
RUN apt-get update && \
    apt-get install -y --no-install-recommends cron tzdata && \
    ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo "UTC" > /etc/timezone && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder image into this runtime image
COPY --from=builder /install /usr/local

# Copy your application code and scripts into the image
COPY app ./app
COPY scripts ./scripts
COPY cron ./cron

# Copy key files into the container
COPY student_private.pem .
COPY student_public.pem .
COPY instructor_public.pem .

# Create volume mount points: /data for seed, /cron for logs
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Install cron job from cron/2fa-cron
# (We will define this file in Step 10; for now just know it's used here)
RUN chmod 644 cron/2fa-cron && crontab cron/2fa-cron

# Expose port 8080 for the API server
EXPOSE 8080

# Start cron daemon AND FastAPI app when container starts
CMD service cron start && \
    uvicorn app.main:app --host 0.0.0.0 --port 8080
