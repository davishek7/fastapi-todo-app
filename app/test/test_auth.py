from .utils import *
from ..services.auth import authenticate_user, create_access_token, get_current_user
from ..configs.database import get_db
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException, status
from ..configs.settings import settings


app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, 'testpassword', db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user("WrongUserName", "testpassword", db)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_user.username, "wrongpassword", db)
    assert wrong_password_user is False

def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)
    
    token = create_access_token(username, user_id, role, expires_delta)

    docoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={'verify_signature': False})

    assert docoded_token['sub'] == username
    assert docoded_token['id'] == user_id
    assert docoded_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():

    encode = {'sub': 'testuser', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    user = await get_current_user(token=token)
    assert user =={'username': 'testuser', 'id': 1, 'user_role': 'admin'}

@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role': 'user'}
    token = jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == 'Could not validate user.'

