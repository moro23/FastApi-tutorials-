from cgitb import text
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel


## create an instance of fastapi
app = FastAPI()

## set the base url 
@app.get("/")
def home_page():
    """
    function to display an output
    """
    return {"data": {"welcome": "<h1> Welcome To Our Page </h1>"}}

## set the blog url 
@app.get('/blog')
def blog(limit: int = 10, published: bool = True):
    
    if published == True:
        return {'data': f'{limit} published posts from the db.'}
    else:
        return {'data': f'{limit} unpublished posts from the db.'}
    

## set the about page url
@app.get("/about")
def about_page():
    return {'data': 'About Page'}


## set url for retriving all unpublished posts
@app.get('/blog/unpublished')
def display_unpublished_posts():
    """
    displays all unpublished posts
    """
    return {'data': 'all unpublished posts'}


## set up a blog url to fetch individual blog post
@app.get('/blog/{id}')
def blog_posts(id: int):
    """
    this function fetchs individual blog post
    id : id of individual blog post
    """
    return {'data': id}


## set url for retriving comments related to a specific post
@app.get('/blog/{id}/comments')
def display_comments(id):
    """
    display comments related to a particular post

    id: id of the post
    """
    return {'data': ['1', '2', '3']}

## define a class for creating a blog post
class Blog(BaseModel):
    title: str
    date: datetime
    body: str

## set url for creating a blog post
@app.post('/blog/create-post')
def create_post(post: Blog):
    return {'data': post}