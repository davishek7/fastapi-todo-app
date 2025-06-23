from fastapi import APIRouter, HTTPException, Path, status
from ..models.todos import Todos
from ..configs.dependency import user_dependency, db_dependency


router = APIRouter(prefix='/admin', tags=['admin'])


@router.get('/todo', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(401, detail='Authentication Failed.')
    return db.query(Todos).all()


@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(401, detail='Authentication Failed.')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(404, "Todo not found!")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()