# app/main.py

from fastapi import FastAPI
from routers import books,magazines, podcasts,theses, videos


app = FastAPI()



app.include_router(books.router)
app.include_router(magazines.router)
app.include_router(theses.router)
app.include_router(podcasts.router)
app.include_router(videos.router)
# app.include_router(users.router)
# app.include_router(auth.router)
# app.include_router(content.router)
# app.include_router(fuzzy_search.router)
