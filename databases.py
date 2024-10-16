import sqlalchemy as sq
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

login = ''
password = ''
name_db = ''


SQLALCHEMY_URL = f'postgresql://{login}:{password}@localhost:5432/{name_db}'

engine = create_engine(SQLALCHEMY_URL)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()