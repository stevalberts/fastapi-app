from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://stevenogwal:secret@localhost:6432/jumia_db")
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://stevenogwal@localhost:6432/jumia_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from .models import Base
    Base.metadata.create_all(bind=engine)