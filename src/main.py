from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.cache.router import router as cache_router
from src.core.database import init_db
from src.core.logging.logging_config import setup_logging
from src.core.logging.sentry import init_sentry
from src.core.router import router as core_router
from src.monsters.router import router as monsters_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_sentry()
    setup_logging()
    print("🚀 Starting application...")
    await init_db()
    print("✅ Database initialized")

    yield

    print("👋 Shutting down application...")


app = FastAPI(
    title="D&D Monsters API",
    description="API для роботи з монстрами D&D, авторизацією та кешуванням",
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(monsters_router)
app.include_router(cache_router)
app.include_router(core_router)


@app.get("/")
async def root():
    return {"message": "D&D Monsters API", "docs": "/docs", "version": "2.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
