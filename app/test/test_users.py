from .utils import *
from ..services.auth import get_current_user
from ..configs.database import get_db
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_current_user


def test_return_user(test_user):
    response = client.get('/user/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'davishek7'
    assert response.json()['email'] == 'davishek7@gmail.com'
    assert response.json()['first_name'] == 'Avishek'
    assert response.json()['last_name'] == 'Das'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '7864047589'

def test_change_password_success(test_user):
    response = client.put('/user/password', json={"password":"testpassword", "new_password":"test1234"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_current_password(test_user):
    response = client.put('/user/password', json={"password":"wrong_password", "new_password":"test1234"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on Password change.'}

def test_change_password_new_password_same_as_current_password(test_user):
    response = client.put('/user/password', json={"password":"testpassword", "new_password":"testpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'New password can not be same as current password.'}

def test_update_phone(test_user):
    response = client.put('/user/phone-number', json={"new_phone_number":"7864047589"})
    assert response.status_code == status.HTTP_204_NO_CONTENT