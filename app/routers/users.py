from fastapi import APIRouter, HTTPException, status
from ..services import users
from ..schemas.users import PasswordChangeRequest, PhoneNumberUpdateRequest
from ..configs.dependency import user_dependency, db_dependency


router = APIRouter(prefix='/user', tags=['users'])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return users.get_user_service(user, db)


@router.put("/phone-number", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_dependency, db: db_dependency, phone_number_update_request: PhoneNumberUpdateRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    users.update_phone_number_service(user, db, phone_number_update_request)
    

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency, db:db_dependency, password_change_request: PasswordChangeRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    users.change_password_service(user, db, password_change_request)
