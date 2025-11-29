# FastAPI RealWorld

RealWorld API implementation with FastAPI + SQLModel, following TDD principles

## 🏗️ Architecture

**Layered Architecture** 사용:
- `app/api/` - API Router Layer (FastAPI endpoints)
- `app/services/` - Service Layer (Business Logic)
- `app/repositories/` - Repository Layer (Data Access)
- `app/models/` - Database Models (SQLModel)
- `app/schemas/` - Pydantic Schemas (Request/Response)
- `app/core/` - Core (Config, DB, Dependencies)

## 🛠️ Tech Stack

- **FastAPI** - Web framework
- **SQLModel** - ORM (SQLAlchemy + Pydantic)
- **uv** - Package manager
- **pytest** - Testing framework
- **ruff** - Linter & Formatter

## 🚀 Setup

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Run linter
uv run ruff check app/

# Run server
uv run uvicorn app.main:app --reload
```

## 📝 Development

TDD (Test-Driven Development) 원칙을 따릅니다:
1. 🔴 **Red** - 실패하는 테스트 작성
2. 🟢 **Green** - 최소한의 코드로 테스트 통과
3. 🔵 **Refactor** - 코드 개선

## 📁 Project Structure

```
fastapi_realworld/
├── app/
│   ├── api/          # API endpoints
│   ├── services/     # Business logic
│   ├── repositories/ # Data access
│   ├── models/       # DB models
│   ├── schemas/      # Pydantic schemas
│   ├── core/         # Config & dependencies
│   └── main.py       # FastAPI app
├── tests/            # Test files
├── pyproject.toml    # Project config
└── README.md
```
