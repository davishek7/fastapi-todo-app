from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from .configs.database import engine, Base
from .routers import auth, todos, admin, users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

Base.metadata.create_all(bind=engine) 

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def index(request: Request):
    return RedirectResponse(url="/todo/todo-page", status_code=status.HTTP_302_FOUND)

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)
app.include_router(admin.router)