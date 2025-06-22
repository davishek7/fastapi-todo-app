from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Annotated
from fastapi import Depends
from os import environ
from dotenv import load_dotenv


load_dotenv()

SQLALCHEMY_DATABASE_URL = environ.get('POSTGRESQL_DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)