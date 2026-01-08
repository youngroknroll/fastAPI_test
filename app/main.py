from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api import article, auth, comment, profile, tag
from app.core.database import create_db_and_tables
from app.core.exceptions import (
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    ValidationException,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (cleanup if needed)


app = FastAPI(title="RealWorld API", version="0.1.0", lifespan=lifespan)


# ============================================================================
# 전역 예외 핸들러
# ============================================================================


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(status_code=404, content={"detail": exc.detail})


@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(status_code=401, content={"detail": exc.detail})


@app.exception_handler(ForbiddenException)
async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(status_code=403, content={"detail": exc.detail})


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(status_code=422, content={"detail": exc.detail})


app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(article.router)
app.include_router(comment.router)
app.include_router(tag.router)


@app.get("/")
def health_check():
    return {"status": "ok"}
