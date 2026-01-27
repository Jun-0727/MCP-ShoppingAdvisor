# ===========================================
# Shopping Advisor MCP Server Dockerfile
# version 1. 도커 이미지 빌드
# ===========================================

# Dockerfile Base Image
FROM python:3.11

# 작업 디렉토리 설정
WORKDIR /app

# uv 설치
RUN pip install uv

# 전체 복사
COPY . .

# 의존성 설치
RUN uv sync

# 서버 실행
CMD ["uv", "run", "uvicorn", "shopping_advisor.server:app", "--host", "0.0.0.0", "--port", "8000"]
