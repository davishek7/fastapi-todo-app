from .utils import *
from fastapi import status
from ..models.todos import Todos
from ..main import app
from ..configs.database import get_db
from ..services.auth import get_current_user


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_current_user


def test_read_all_authenticated(test_todo):
    response = client.get("/todo/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'title': "Learn FastAPI", 'description': "It is a great Python Framework", 
                                'priority': 5, 'complete': False, 'owner_id': 1, 'id': 1}]
    
def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'title': "Learn FastAPI", 'description': "It is a great Python Framework", 
                                'priority': 5, 'complete': False, 'owner_id': 1, 'id': 1}
    
def test_read_all_authenticated_not_found():
    response = client.get("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found!'}

def test_create_todo(test_todo):
    request_data = {
        'title': 'New Todo', 
        'description': 'New Todo Description', 
        'priority': 5, 
        'complete': False, 
        'owner_id': 1
    }
    response = client.post("/todo", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')
    assert model.owner_id == request_data.get('owner_id')

def test_update_todo(test_todo):
    request_data={
        'title': "Change the title of the todo already saved!", 
        'description': "It is a great Python Framework", 
        'priority': 5, 
        'complete': False, 
        'owner_id': 1
    }

    response = client.put("/todo/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == 'Change the title of the todo already saved!'

def test_update_todo_not_found():
    request_data={
        'title': "Change the title of the todo already saved!", 
        'description': "It is a great Python Framework", 
        'priority': 5, 
        'complete': False, 
        'owner_id': 1
    }

    response = client.put("/todo/999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found!'}


def test_delete_todo(test_todo):
    response = client.delete("/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_not_found():
    response = client.delete("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found!'}

