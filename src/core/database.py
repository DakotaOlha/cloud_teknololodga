from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, func
from datetime import datetime
from contextlib import asynccontextmanager

from src.core.settings import settings


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    """Mixin для автоматичного додавання created_at та updated_at"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


# Створення асинхронного engine
engine = create_async_engine(
    settings.postgres,
    echo=True,
    pool_pre_ping=True
)

# Створення sessionmaker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db() -> AsyncSession:
    """Dependency для отримання сесії бази даних"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Ініціалізація бази даних (створення таблиць)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)