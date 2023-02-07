from blog.routers import authentication
from fastapi import FastAPI

from . import  models
from .database import  engine

from .routers import blogs, users, authentication

## migrating the tables in the db 
models.Base.metadata.create_all(bind=engine) 

## creating an instance of FastAPI
app = FastAPI()

## defining login routes
app.include_router(authentication.router)

## defining all blog posts routes
app.include_router(blogs.router)

## defining all the users  routes
app.include_router(users.router)

