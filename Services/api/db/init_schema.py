#!/usr/bin/env python3
"""
Initialize complete database schema.
Creates all tables with proper relationships and indexes.
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from services.api.db.postgres import engine, Base
from services.api.db.schema import Video, Job, VideoVariant, Thumbnail


async def init_schema():
    """Initialize all database tables."""
    print("🗄️  Initializing database schema...")
    print("=" * 50)
    
    async with engine.begin() as conn:
        # Drop all tables (use with caution!)
        # await conn.run_sync(Base.metadata.drop_all)
        # print("⚠️  Dropped existing tables")
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Created tables:")
        print("   - videos")
        print("   - jobs")
        print("   - video_variants")
        print("   - thumbnails")
    
    print("\n📊 Schema Summary:")
    print(f"   Total tables: {len(Base.metadata.tables)}")
    
    for table_name, table in Base.metadata.tables.items():
        print(f"\n   Table: {table_name}")
        print(f"   Columns: {len(table.columns)}")
        print(f"   Indexes: {len(table.indexes)}")
        print(f"   Foreign Keys: {len(table.foreign_keys)}")
    
    print("\n✅ Database schema initialized successfully!")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_schema())
