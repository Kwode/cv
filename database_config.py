from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

DATABASE_URL = 'postgresql://postgres:#Girlpower4life@localhost/cvapp'

engine  = create_engine(DATABASE_URL)

session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
