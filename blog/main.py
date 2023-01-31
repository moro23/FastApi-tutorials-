from typing import List
from urllib import request
from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from . import  models, schemas, hashing
from .database import  SessionLocal, engine

## migrating the tables in the db 
models.Base.metadata.create_all(bind=engine) 

## creating an instance of FastAPI
app = FastAPI()

## creating db connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def createBlog(request: schemas.Blog, db: Session = Depends(get_db)):
    """
    Creating blog post
    """
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
def getAllBlogPost(db: Session = Depends(get_db)):
    """
    List all blog post
    """
    all_posts = db.query(models.Blog).all()
    return all_posts

@app.get('/blog/{id}', response_model=schemas.ShowBlog, tags=['blogs'])
def getIndividualPost(id, db: Session = Depends(get_db)):
    """
    Retrive individual post with a specific id
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog post with the {'title'} not available")
    return blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def deletePost(id, db: Session = Depends(get_db)):
    """
    Deleting a blog post with a specific id

    id: int
    db: db session
    """
    blog_post = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog_post:
        raise HTTPException(status_code=404, detail="Blog post with the {'title'} not available")
    
    blog_post.delete(synchronize_session=False)
    db.commit()

    return f"Blog post with the {'Title'} Deleted."

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def updatePost(id, request: schemas.Blog, db: Session = Depends(get_db)):
    """
    Updating a blog post with a specific id

    id: int
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog post with the {'title'} not available")
    
    blog.update(request, synchronize_session=False)
    db.commit()

    return f"Blog post with the {'Title'} Updated."



@app.post('/user', response_model=schemas.ShowUser, tags=["users"])
def createUser(request: schemas.User, db: Session = Depends(get_db)):
    """
    Creating a User 
    """
    ## lets hash the password coming from the user
    #hashed_password = pwd_context.hash(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}', response_model=schemas.ShowUser, tags=["users"])
def getUser(id:int, db: Session = Depends(get_db)):
    """
    Retrive an individual user with a specific id
    """
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with the {'name'} not available")
    return user