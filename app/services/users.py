from fastapi import HTTPException
from ..services.auth import bcrypt_context
from ..models.users import Users


def get_user_service(user, db):
    return db.query(Users).filter(Users.id == user.get('id')).first()

def update_phone_number_service(user, db, phone_number_update_request):
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number_update_request.new_phone_number
    db.commit()

def change_password_service(user, db, password_change_request):
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(password_change_request.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Error on Password change.")
    
    if bcrypt_context.verify(password_change_request.new_password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="New password can not be same as current password.")
    
    user_model.hashed_password = bcrypt_context.hash(password_change_request.new_password)
    db.commit()