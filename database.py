from sqlalchemy import (
    create_engine,
)  # It is connector to link python application and database
from sqlalchemy.orm import sessionmaker, declarative_base

# to create a session and also base class for all ORM models
from dotenv import load_dotenv

# to load enivronment variables from .env
import os

# load our environment into the program
load_dotenv()
# this get connection string from env
DATABASE_URL = os.getenv("DATABASE_URL")

# with url, we can create a database engine
engine = create_engine(DATABASE_URL)

# now we need to create a session
# so we are binding our engine with session
session_local = sessionmaker(bind=engine,autoflush=False)

# construct base class for our ORM model class
custom_base = declarative_base()