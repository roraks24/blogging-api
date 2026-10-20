from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os

# Default to /tmp/blog.db if running on serverless Vercel, else local blog.db
default_sqlite = "sqlite:////tmp/blog.db" if os.environ.get("VERCEL") else "sqlite:///./blog.db"
DATABASE_URL = os.getenv("DATABASE_URL", default_sqlite)

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

sessionlocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
