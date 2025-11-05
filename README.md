```bash
# 프로젝트 구조
fastAPI_realworld/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 엔트리포인트
│   ├── api/                    # 라우터 모듈
│   │   ├── __init__.py
│   │   └── article.py
│   ├── core/                   # 설정/환경/의존성 (Config, DB 등)
│   │   ├── __init__.py
│   │   └── config.py
│   ├── models/                 # ORM 모델 (SQLAlchemy, SQLModel 등)
│   │   ├── __init__.py
│   │   └── article.py
│   ├── schemas/                # Pydantic 스키마
│   │   ├── __init__.py
│   │   └── article.py
│   └── services/               # 비즈니스 로직
│       ├── __init__.py
│       └── article_service.py
│
├── tests/                      # pytest 테스트 코드
│   ├── __init__.py
│   └── test_article_api.py
│
├── pyproject.toml              # uv + Ruff + Pytest 설정
├── uv.lock
├── Makefile                    # lint/test/serve 단축 명령
├── Dockerfile                  # (추후 CI/CD용)
└── README.md
```