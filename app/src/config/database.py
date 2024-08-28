from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from app.src.config.settings import get_settings

settings = get_settings()

if settings.DATABASE_URL.startswith('postgres://'):
    settings.DATABASE_URL = settings.DATABASE_URL.replace('postgres://', 'postgresql://')

engine = create_engine(
    url=settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=100,
    max_overflow=50,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DBBase = declarative_base()