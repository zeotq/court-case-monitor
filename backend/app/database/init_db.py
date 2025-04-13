from app.database.base import Base
from app.database.engine import engine
from app.config import DATABASE_DROP_ALL


def init_db():
    try:
        if DATABASE_DROP_ALL:
            print("[INFO] Dropping all tables...")
            Base.metadata.drop_all(bind=engine)

        Base.metadata.create_all(bind=engine)
        print("[SUCCESS] Tables created!")
        print(f"[INFO] Tables list: {list(Base.metadata.tables.keys())}")
    except Exception as e:
        print(f"[ERROR] Error while creating tables {str(e)}")
    finally:
        engine.dispose()