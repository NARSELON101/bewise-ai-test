from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.postgresql import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


SQLALCHEMY_POSTGRES_URL = (f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@'
                           f'{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}')

engine = create_async_engine(SQLALCHEMY_POSTGRES_URL, pool_size=10, max_overflow=20, pool_recycle=3600)
sync_maker = sessionmaker()
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, sync_session_class=sync_maker)


async def get_postgres_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class Base(DeclarativeBase):
    pass
