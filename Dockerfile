# ===========================================
# Shopping Advisor MCP Server Dockerfile
# version 4. 멀티 스테이지 빌드 도입
# ===========================================

# ===========================================
# Builde Stage
# ===========================================

# Dockerfile Base Image - 빌드
FROM python:3.11-slim AS builder

# 빌드에 필요한 env 설정
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# 작업 디렉토리 설정
WORKDIR /app

# uv 설치(only 빌드 스테이지)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 의존성 파일 복사
COPY pyproject.toml uv.lock* ./

# 의존성 설치
RUN uv sync --no-dev --no-install-project


# ===========================================
# Runtime Stage
# ===========================================

# Dockerfile Base Image - 런타임
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 런타임에 필요한 env 설정
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

# 필요한 파일 복사(빌드 스테이지 참조)
COPY --from=builder /app/.venv ./.venv
COPY src ./src

# 서버 실행
CMD ["uvicorn", "shopping_advisor.server:app", "--host", "0.0.0.0", "--port", "8000"]
