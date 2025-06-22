from fastapi import APIRouter, Depends, HTTPException, Path, Query
from typing import Annotated
from ..models import Users
from ..database import SessionLocal
from starlette import status
from pydantic import BaseModel, Field
from .auth import bcrypt_context
from .auth import get_current_user
from sqlalchemy.orm import Session


router = APIRouter(prefix='/user', tags=['users'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class PasswordChangeRequest(BaseModel):
    password: str
    new_password: str


class PhoneNumberUpdateRequest(BaseModel):
    new_phone_number: str


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put("/phone-number", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_dependency, db: db_dependency, phone_number_update_request: PhoneNumberUpdateRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number_update_request.new_phone_number
    db.commit()
    

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency, db:db_dependency, password_change_request: PasswordChangeRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(password_change_request.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Error on Password change.")
    
    if bcrypt_context.verify(password_change_request.new_password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="New password can not be same as current password.")
    
    user_model.hashed_password = bcrypt_context.hash(password_change_request.new_password)
    db.commit()
