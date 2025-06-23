from fastapi import APIRouter, Request, Depends
from typing import Annotated
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from ..schemas.auth import CreateUserRequest, Token
from ..services import auth
from ..configs.dependency import db_dependency



router = APIRouter(prefix='/auth', tags=['auth'])

templates = Jinja2Templates(directory="app/templates")

#Pages

@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


#Endpoints

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency, create_user_request: CreateUserRequest):
    auth.create_user_service(db, create_user_request)


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    return auth.login_for_access_token_service(form_data, db)