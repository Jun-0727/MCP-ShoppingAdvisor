# Smart Shopping Advisor MCP

**"도움은 AI가, 선택·판단은 사용자가"**

구매할 물품을 입력하면 제품의 특징, 장단점, 구매 시 주의사항과 함께  
각 쇼핑몰별 장단점 및 구매 링크를 제공하는 지능형 쇼핑 의사결정 지원 MCP 서버

<br>

## 데모

**[▶ 지금 바로 사용해보기](https://playmcp.kakao.com/mcp/471)**

<br>

## 핵심 기능

### 1. 제품 상세 분석 (`get_product`)
```
📦 제품 정보 제공
├─ 주요 특징 및 사양
├─ 장점 / 단점 정리
└─ 구매 전 주의사항 (정품 확인, AS 정책 등)
```

### 2. 쇼핑 가이드 생성 (`create_shopping_guide`)
```
🛒 지원 쇼핑몰 : 쿠팡, 네이버 쇼핑, SSG, G마켓, 무신사, 알리익스프레스 등
```
각 쇼핑몰별로 다음 정보를 제공합니다:
- 장점 (배송 속도, 반품 정책, 가격 경쟁력 등)
- 단점 (품절 가능성, 배송 기간, 가격대 등)
- 제품 검색 직링크

### 3. 제품 비교 (`compare_products`)
```
⚖️ 비교 분석 제공
├─ 항목별 사양 비교표
├─ 제품별 장단점 요약
└─ 사용 목적별 추천
```

<br>

## 기술 스택

| 분류 | 기술 |
|------|------|
| Language | Python 3.11 |
| Framework | FastAPI, FastMCP |
| Server | Uvicorn (ASGI) |
| AI | OpenAI API |
| Cache | LRU 메모리 캐시 + SQLite |
| Container | Docker, Docker Compose |
| Package Manager | uv |

<br>

## 시작하기

### 사전 요구사항

- [Docker](https://www.docker.com/) 및 Docker Compose
- OpenAI API Key

### 1. 저장소 클론

```bash
git clone <repository-url>
cd shopping_advisor
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 아래 내용을 채웁니다.

```bash
cp .env.example .env
```

```env
# OpenAI API Key (필수)
OPENAI_API_KEY=sk-...

# 서버 설정
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
BASE_URL=http://localhost:8000

# 캐시 설정
CACHE_DB_PATH=data/product_cache.db
CACHE_EXPIRE_DAYS=30
MEMORY_CACHE_SIZE=1000

# CORS 설정
ALLOWED_ORIGINS=*

# 기타
LOG_LEVEL=INFO
ENVIRONMENT=production
```

### 3. Docker로 실행

```bash
docker compose up -d
```

서버가 정상 실행되면 `http://localhost:8000`에서 접근할 수 있습니다.

```bash
# 서버 상태 확인
curl http://localhost:8000/health

# 로그 확인
docker compose logs -f
```

### 4. 서버 중지

```bash
docker compose down
```

<br>

## 환경 변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `OPENAI_API_KEY` | OpenAI API 키 (필수) | - |
| `SERVER_PORT` | 서버 포트 | `8000` |
| `CACHE_DB_PATH` | SQLite 캐시 파일 경로 | `data/product_cache.db` |
| `CACHE_EXPIRE_DAYS` | 캐시 유효 기간 (일) | `30` |
| `MEMORY_CACHE_SIZE` | 메모리 LRU 캐시 최대 항목 수 | `1000` |
| `ALLOWED_ORIGINS` | CORS 허용 오리진 | `*` |
| `LOG_LEVEL` | 로그 레벨 | `INFO` |

<br>

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `POST` | `/mcp` | MCP JSON-RPC 요청 처리 |
| `GET` | `/mcp` | SSE 스트림 (keep-alive) |
| `GET` | `/health` | 헬스 체크 |
| `GET` | `/.well-known/mcp.json` | MCP 서버 매니페스트 |

MCP 클라이언트 연결 설정:
```json
{
  "mcpServers": {
    "shopping-advisor": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

<br>

## 사용 예시

### 예시 1: 제품 정보 조회

**입력**
```
마샬 블루투스 스피커 추천해줘
```

**출력**
```markdown
# 마샬 블루투스 스피커

## 제품 특징
- 빈티지 감성의 독특한 디자인
- 마샬 특유의 저음 강조 사운드
- 휴대용(Emberton)부터 대형(Woburn)까지 다양한 라인업

## 장점
- 디자인 만족도가 매우 높음
- 브랜드 사운드 아이덴티티가 확실함
- 내구성이 우수함

## 단점
- 가격 대비 음질 성능 논란 있음
- 병행수입 제품의 경우 AS 불편
- 무게감이 있어 휴대성 제한적

## 구매 전 체크리스트
- 정품/공식 유통 여부 확인
- 방수 등급(IPX7 등) 확인
- AS 정책 및 기간 확인
```

### 예시 2: 쇼핑 가이드 생성

**출력**
```markdown
## 쇼핑몰별 비교

| 쇼핑몰 | 장점 | 단점 | 추천 상황 |
|--------|------|------|-----------|
| 쿠팡 | 로켓배송, 무료반품 | 인기 모델 품절 잦음 | 빠른 배송 필요 시 |
| 네이버쇼핑 | 가격 비교 용이 | 판매자별 정책 상이 | 가격 비교 원할 때 |
| SSG | 정품 신뢰도 높음 | 가격대 다소 높음 | AS 중요할 때 |
```

<br>

## 프로젝트 구조

```
shopping-advisor/
├── Dockerfile                          # 멀티 스테이지 빌드 (builder + runtime)
├── docker-compose.yml                  # 컨테이너 실행 설정
├── pyproject.toml                      # 프로젝트 메타데이터 및 의존성
├── uv.lock                             # 버전 잠금 파일
├── .env                                # 환경 변수 (git 제외)
├── .dockerignore
├── data/
│   ├── product_cache.db                # SQLite 캐시 DB
│   └── shopping_malls.json             # 쇼핑몰 정보
├── logs/
│   ├── shopping_advisor.log
│   └── error.log
├── src/
│   └── shopping_advisor/
│       ├── server.py                   # FastAPI 앱 및 MCP 엔드포인트
│       ├── logging_config.py           # 로깅 설정
│       └── utils/
│           ├── tool.py                 # MCP 툴 정의 (get_product 등)
│           ├── cache_manager.py        # 2계층 캐시 (메모리 LRU + SQLite)
│           ├── gpt_api.py              # OpenAI API 연동
│           ├── prompt_template.py      # 프롬프트 템플릿
│           ├── shopping_mall.py        # 쇼핑몰 URL 생성 및 정보
│           └── formatter.py            # 응답 포맷 변환
└── tests/
    └── manual_tests/
        ├── test_cache_manager.py       # 캐시 매니저 테스트
        ├── test_formatter.py           # 포맷터 테스트
        ├── test_gpt_api.py             # GPT API 테스트
        └── test_shopping_mall.py       # 쇼핑몰 유틸 테스트
```

<br>

## 캐시 구조

API 호출 비용 절감 및 응답 속도 향상을 위해 2계층 캐시를 사용합니다.

```
요청
 │
 ▼
[1차] 메모리 캐시 (LRU, 최대 1,000개)
 │ 미스
 ▼
[2차] SQLite 캐시 (만료: 30일)
 │ 히트 → 메모리에 write-back
 │ 미스
 ▼
OpenAI API 호출 → 캐시 저장
```

<br>

## 법적 고지

본 프로젝트는 **웹 스크래핑, 크롤링, 자동화된 데이터 수집을 수행하지 않습니다.**

**하는 것**
- 공개된 쇼핑몰 검색 URL 생성
- 일반적인 제품 특성 정보 제공 (AI 생성)
- 쇼핑몰별 공개된 정책 정보 요약

**하지 않는 것**
- 실시간 가격 정보 수집
- 재고 현황 크롤링
- 리뷰 데이터 스크래핑
- 개인정보 수집 및 저장

> 모든 쇼핑몰 링크는 제품명 기반의 공개 검색 URL 템플릿을 조합하여 생성되며, 자동화된 접근이나 데이터 추출 목적이 아닙니다.
