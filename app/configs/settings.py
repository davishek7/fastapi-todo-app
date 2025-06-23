from pydantic_settings import BaseSettings
from os import environ
from dotenv import load_dotenv


load_dotenv() 

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = environ.get('POSTGRESQL_DATABASE_URL')
    SECRET_KEY: str = environ.get('SECRET_KEY')
    ALGORITHM: str = environ.get('ALGORITHM')


settings = Settings()