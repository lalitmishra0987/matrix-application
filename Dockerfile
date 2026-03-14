# ── Stage 1: builder ──────────────────────────────────────────────
FROM alpine:3.19 AS builder

RUN apk add --no-cache \
    python3 \
    py3-pip \
    git

ARG REPO_URL="https://github.com/lalitmishra0987/matrix-application.git"
ARG BRANCH="main"

RUN git clone --branch ${BRANCH} --single-branch ${REPO_URL} /build

WORKDIR /build

# Create venv at the exact path it will live in the runtime stage
RUN python3 -m venv /app/venv

# Install all packages into the venv
RUN /app/venv/bin/pip install --upgrade pip \
    && /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Verify gunicorn is actually there before we leave the builder
RUN ls -la /app/venv/bin/gunicorn


# ── Stage 2: runtime ──────────────────────────────────────────────
FROM alpine:3.19 AS runtime

LABEL maintainer="platform-team" \
    description="Matrix rain — terminal + web" \
    version="2.0.0"

RUN apk add --no-cache \
    python3 \
    libffi

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TERM=xterm-256color \
    COLORTERM=truecolor \
    PATH="/app/venv/bin:$PATH" \
    VIRTUAL_ENV=/app/venv

# Create non-root user
RUN adduser -D -u 1001 appuser

# Copy venv from builder — must happen before USER switch
COPY --from=builder /app/venv /app/venv

# Copy app files from cloned repo
COPY --from=builder /build/matrix_app.py /app/
COPY --from=builder /build/app.py /app/
COPY --from=builder /build/templates /app/templates/

# Set ownership of everything under /app to appuser
RUN chown -R appuser:appuser /app

WORKDIR /app

USER appuser

EXPOSE 8080

ENTRYPOINT ["/app/venv/bin/gunicorn"]
CMD ["--bind", "0.0.0.0:8080", "--workers", "4", "app:app"]