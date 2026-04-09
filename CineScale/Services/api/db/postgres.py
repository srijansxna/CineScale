from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from services.api.config import get_settings

settings = get_settings()

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True
)

# Create async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Dependency for getting async database session."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database tables and apply any missing column migrations."""
    # Import models so SQLAlchemy registers them with Base.metadata
    from services.api.db import pg_models  # noqa: F401
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Safely add columns introduced after initial schema creation
        migrations = [
            "ALTER TABLE videos ADD COLUMN IF NOT EXISTS video_title VARCHAR",
            "ALTER TABLE videos ADD COLUMN IF NOT EXISTS default_thumbnail VARCHAR",
            "ALTER TABLE videos ADD COLUMN IF NOT EXISTS final_thumbnail_path VARCHAR",
        ]
        for sql in migrations:
            await conn.execute(__import__('sqlalchemy').text(sql))
