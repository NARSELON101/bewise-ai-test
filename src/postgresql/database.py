from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.postgresql import settings


SQLALCHEMY_POSTGRES_URL = (f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@'
                           f'{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}')

engine = create_engine(SQLALCHEMY_POSTGRES_URL, pool_size=10, max_overflow=20, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_postgres_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    pass


Base.metadata.create_all(engine)
