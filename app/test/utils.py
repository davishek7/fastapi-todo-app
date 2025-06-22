from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..models import Base
from fastapi.testclient import TestClient
from ..models import Todos, Users
import pytest
from ..main import app
from ..routers.auth import bcrypt_context


SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_current_user():
    return {'username': 'admin', 'id': 1, 'user_role': 'admin'}


client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(title="Learn FastAPI", description="It is a great Python Framework", priority=5, complete=False, owner_id=1)
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        username="davishek7",
        email="davishek7@gmail.com",
        first_name="Avishek",
        last_name="Das",
        hashed_password = bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number = "7864047589"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()

