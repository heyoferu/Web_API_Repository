# app/main.py

from fastapi import FastAPI
from routers import users, auth, content


app = FastAPI()


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(content.router)
