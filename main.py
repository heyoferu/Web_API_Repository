# app/main.py

from fastapi import FastAPI
from routers import books,magazines, podcasts, search,theses, videos

app = FastAPI()

app.include_router(books.router)
app.include_router(magazines.router)
app.include_router(theses.router)
app.include_router(podcasts.router)
app.include_router(videos.router)
app.include_router(search.router)

