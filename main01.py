from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

import logging
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="homework5/templates")


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


class UserIn(BaseModel):
    name: str
    email: str
    password: str


users = [
    User(id=i, name=f"Name{i}", email=f"Email{i}", password="123") for i in range(1, 11)
]


@app.get("/")
async def index():
    return {"message": "Hello"}


@app.get("/users/", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse(
        "users.html", {"request": request, "users": users}
    )


@app.post("/users/", response_class=HTMLResponse)
async def delete_user(request: Request):
    form_data = await request.form()
    for user in users:
        if int(form_data.get("user_id")) == user.id:
            users.remove(user)
            break
    return templates.TemplateResponse(
        "users.html", {"request": request, "users": users}
    )


@app.get("/users/new_user", response_class=HTMLResponse)
async def new_user(request: Request):
    return templates.TemplateResponse("post_user_form.html", {"request": request})


@app.post("/users/new_user", response_class=HTMLResponse)
async def post_user(request: Request):
    form_data = await request.form()
    users.append(
        User(
            id=users[len(users) - 1].id + 1,
            name=form_data.get("name"),
            email=form_data.get("email"),
            password=form_data.get("password"),
        )
    )
    return templates.TemplateResponse("success_added.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("main01:app", host="127.0.0.1", port=8000, reload=True)
