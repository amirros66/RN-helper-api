from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "postgresql://rozruhaw:HyVeZ2B2axtTkkO1LAEEy3CTpJ4gpei2@horton.db.elephantsql.com/rozruhaw"
DATABASE_URL = "postgresql://postgres:secret@localhost:5446/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()