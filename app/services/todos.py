from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse
from ..services.auth import get_current_user
from ..models.todos import Todos


def get_todos_service(user, db):
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

def get_todo_service(user, db, todo_id):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found!')

def create_todo_service(user, db, todo_request):
    todo_model = Todos(**todo_request.model_dump(), owner_id = user.get('id'))
    db.add(todo_model)
    db.commit()

def update_todo_service(user, db, todo_request, todo_id):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(404, "Todo not found!")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

def delete_todo_service(user, db, todo_id):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(404, "Todo not found!")
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()
    db.commit()

def redirect_to_login():
    redirect_response = RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie('access_token')
    return redirect_response

async def render_todo_page_service(request, db):
    user = await get_current_user(request.cookies.get('access_token'))

    if user is None:
        return redirect_to_login()
    
    todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

    return user, todos

async def render_add_todo_page(request):
    user = await get_current_user(request.cookies.get('access_token'))

    if user is None:
        return redirect_to_login()
    
    return user

async def render_edit_todo_page(request, db, todo_id):
    user = await get_current_user(request.cookies.get('access_token'))

    if user is None:
        redirect_to_login()

    todo = get_todo_service(user, db, todo_id)

    return user, todo
    