from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.db.init_db import init_db
from app.db.session import SessionLocal

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description=(
        "NHJ AI construction platform — v0.1 executable foundation. "
        "See /docs for the interactive API reference."
    ),
)

# Wide open by default so the frontend works regardless of which domain it
# ends up deployed on in v0.1. Narrow this to the real frontend origin(s)
# via settings.CORS_ORIGINS before any production deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()


@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok", "service": settings.PROJECT_NAME}


app.include_router(api_router, prefix=settings.API_V1_PREFIX)

