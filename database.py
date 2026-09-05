from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
# Convert to use psycopg2 (synchronous)
SYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql://").replace("postgresql+asyncpg://", "postgresql://")

engine = create_engine(SYNC_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()