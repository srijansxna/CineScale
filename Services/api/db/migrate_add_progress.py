#!/usr/bin/env python3
"""
Migration script to add progress column to processing_jobs table.
"""
import asyncio
from sqlalchemy import text
from services.api.db.postgres import engine


async def migrate():
    """Add progress column to processing_jobs table."""
    async with engine.begin() as conn:
        # Check if column exists
        result = await conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='processing_jobs' 
            AND column_name='progress'
        """))
        
        if result.fetchone() is None:
            print("Adding progress column to processing_jobs table...")
            await conn.execute(text("""
                ALTER TABLE processing_jobs 
                ADD COLUMN progress INTEGER DEFAULT 0 NOT NULL
            """))
            print("✅ Progress column added successfully!")
        else:
            print("✅ Progress column already exists")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(migrate())
