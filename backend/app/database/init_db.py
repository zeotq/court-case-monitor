from app.database.base import Base
from app.database.engine import engine

# from app.models.user import UserDB  
# from app.models.task import TaskDB
# from app.models.organisation import OrganisationDB
# from app.models import association_tables


def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("[SUCCESS] Tables created!")
        print(f"Tables list: {list(Base.metadata.tables.keys())}")
    except Exception as e:
        print(f"[ERROR] Error while creating tables {str(e)}")
    finally:
        engine.dispose()