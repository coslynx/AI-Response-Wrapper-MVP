from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from app.config import settings

# Define the SQLAlchemy base class for database models
Base = declarative_base()

# Create the SQLAlchemy engine using the database connection string
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency function to inject a database session into API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()