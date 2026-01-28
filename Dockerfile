# ===========================================
# Shopping Advisor MCP Server Dockerfile
# version 2. 이미지 용량 최적화 및 레이어 캐싱
# ===========================================

# Dockerfile Base Image: python slim 버전 사용으로 이미지 크기 감소
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# uv 설치
RUN pip install uv

# 의존성 파일 먼저 복사
COPY pyproject.toml uv.lock* ./

# 의존성 설치
# --no-dev 옵션 추가로 개발 의존성 제외
# --no-install-project 옵션 추가로 프로젝트 자체 설치 제외(src 없이 sync 가능)
RUN uv sync --no-dev --no-install-project

# 소스코드 복사
COPY src ./src

# 서버 실행
CMD ["uv", "run", "uvicorn", "shopping_advisor.server:app", "--host", "0.0.0.0", "--port", "8000"]
