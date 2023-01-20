from fastapi import FastAPI

from .schemas import Blog


from . import  models
from .database import  engine

## migrating the tables in the db
models.Base.metadata.create_all(bind=engine)

## creating an instance of FastAPI
app = FastAPI()


@app.post('/blog')
def createBlog(request: Blog):
    return request 