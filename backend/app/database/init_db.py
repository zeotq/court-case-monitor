import asyncio
from app.database.base import Base
from app.database.engine import engine
from app.config import DATABASE_DROP_ALL

async def init_db():
    try:
        async with engine.begin() as conn:
            if DATABASE_DROP_ALL:
                print("[INFO] Dropping all tables...")
                await conn.run_sync(Base.metadata.drop_all)

            await conn.run_sync(Base.metadata.create_all)
            print("[SUCCESS] Tables created!")
            print(f"[INFO] Tables list: {list(Base.metadata.tables.keys())}")
    except Exception as e:
        print(f"[ERROR] Error while creating tables: {str(e)}")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())
