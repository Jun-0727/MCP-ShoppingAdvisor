# ===========================================
# Shopping Advisor MCP Server Dockerfile
# version 3. uv 관련 최적화(설치 및 실행)
# ===========================================

# Dockerfile Base Image
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# uv 설치 방법 변경
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 의존성 파일 복사
COPY pyproject.toml uv.lock* ./

# 의존성 설치
RUN uv sync --no-dev --no-install-project

# venv PATH 주입
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

# 소스코드 복사
COPY src ./src

# uv 없이 직접 서버 실행
CMD ["uvicorn", "shopping_advisor.server:app", "--host", "0.0.0.0", "--port", "8000"]
