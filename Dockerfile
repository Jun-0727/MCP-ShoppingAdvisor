# ===========================================
# Shopping Advisor MCP Server Dockerfile
# version 5. 보안 및 권한 최적화 
# ===========================================

# ===========================================
# Builde Stage
# ===========================================

# Dockerfile Base Image
FROM python:3.11-slim AS builder

# 빌드에 필요한 env 설정
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/app/.venv/bin:$PATH"

# 작업 디렉토리 설정
WORKDIR /app

# uv 설치
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 의존성 파일 복사
COPY pyproject.toml uv.lock* ./

# 의존성 설치
RUN uv sync --no-dev --no-install-project


# ===========================================
# Runtime Stage
# ===========================================

# Dockerfile Base Image
FROM python:3.11-slim

# non-root 유저 생성
RUN useradd --create-home --shell /bin/bash appuser

# 작업 디렉토리 설정
WORKDIR /app

# 런타임에 필요한 env 설정
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

# .venv 복사
COPY --from=builder /app/.venv ./.venv

# 소스코드 복사 + 권한 설정
COPY --chown=appuser:appuser src ./src

# logs 디렉토리 생성
RUN mkdir -p logs && chown appuser:appuser logs

# 유저 설정
USER appuser

EXPOSE 8000

# 서버 실행
CMD ["uvicorn", "shopping_advisor.server:app", "--host", "0.0.0.0", "--port", "8000"]
