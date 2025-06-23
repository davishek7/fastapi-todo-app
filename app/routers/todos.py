from fastapi import APIRouter, HTTPException, Path, status
from ..services import todos
from ..schemas.todos import TodoRequest
from ..configs.dependency import user_dependency, db_dependency


router = APIRouter(prefix='/todo', tags=['todos'])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_todos(user:user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return todos.get_todos_service(user, db)


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo(user:user_dependency, db:db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return todos.get_todo_service(user, db, todo_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(user:user_dependency, db:db_dependency, todo_request:TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todos.create_todo_service(user, db, todo_request)


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user:user_dependency, db: db_dependency, todo_request:TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todos.update_todo_service(user, db, todo_request, todo_id)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency, db: db_dependency, todo_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todos.delete_todo_service(user, db, todo_id)