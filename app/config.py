from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://stevenogwal:secret@localhost:6432/jumia_db")
# # DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://stevenogwal@localhost:6432/jumia_db")
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Load Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials in .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# def init_db():
#     from .models import Base
#     Base.metadata.create_all(bind=engine)