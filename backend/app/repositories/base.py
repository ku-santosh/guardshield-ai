from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from backend.app.config import settings

Base = declarative_base()

# Initialize Async Engine conditionally safely
engine = None
AsyncSessionLocal = None

if settings.USE_DATABASE and settings.ASYNC_DATABASE_URL:
    engine = create_async_engine(settings.ASYNC_DATABASE_URL, pool_pre_ping=True, future=True)
    AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def db_session():
    """
    Dependency to get an async database session.
    """
    if not settings.USE_DATABASE or not AsyncSessionLocal:
        yield None
        raise RuntimeError("Database usage is disabled. Check your configuration.")
        # return
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e