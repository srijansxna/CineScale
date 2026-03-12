#!/usr/bin/env python3
"""
Database initialization script.
Run this to create all tables in PostgreSQL.
"""
import asyncio
from services.api.db.postgres import init_db, engine
from services.api.db.pg_models import Video, ProcessingJob


async def main():
    """Initialize database tables."""
    print("Creating database tables...")
    await init_db()
    print("✅ Database tables created successfully!")
    
    # Close engine
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
