from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.core.database import init_db
from src.auth.router import router as auth_router
from src.monsters.router import router as monsters_router
from src.cache.router import router as cache_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler"""
    # Startup
    print("🚀 Starting application...")
    # Міграції тепер запускаються в docker-compose command
    await init_db()
    print("✅ Database initialized")

    yield

    # Shutdown
    print("👋 Shutting down application...")


app = FastAPI(
    title="D&D Monsters API",
    description="API для роботи з монстрами D&D, авторизацією та кешуванням",
    version="2.0.0",
    lifespan=lifespan
)

# Підключення роутерів
app.include_router(auth_router)
app.include_router(monsters_router)
app.include_router(cache_router)


@app.get("/")
async def root():
    return {
        "message": "D&D Monsters API",
        "docs": "/docs",
        "version": "2.0.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}