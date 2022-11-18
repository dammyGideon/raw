from fastapi import FastAPI
from app.routes.todos import todo_router
from app.routes.posts import post_router
from app.database.connection import connection
from app.database.db import get_db
from app.models import posts

from app.database.db import engine

posts.Base.metadata.create_all(bind=engine)



app = FastAPI()
get_db()

connection()

app.include_router(todo_router)
app.include_router(post_router)




