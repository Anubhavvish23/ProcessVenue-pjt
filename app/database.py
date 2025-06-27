from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Skit%401234@localhost:5432/bookdb")

# ✅ Create the engine
engine = create_engine(DATABASE_URL)

# ✅ Session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ This is what Alembic is trying to import
Base = declarative_base()

# ✅ Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
