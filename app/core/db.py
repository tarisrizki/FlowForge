from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# Create async engine for PostgreSQL
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Session factory
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    """Dependency for getting async database session"""
    async with AsyncSessionLocal() as session:
        yield session
