from app.database.base import Base
from app.database.engine import engine


def init_db():
    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("[SUCCESS] Tables created!")
        print(f"Tables list: {list(Base.metadata.tables.keys())}")
    except Exception as e:
        print(f"[ERROR] Error while creating tables {str(e)}")
    finally:
        engine.dispose()