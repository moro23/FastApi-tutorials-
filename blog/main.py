from typing import List
from urllib import request
from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from . import  models, schemas
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


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def createBlog(request: schemas.Blog, db: Session = Depends(get_db)):
    """
    Creating blog post
    """
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', response_model=List[schemas.ShowBlog])
def getAllBlogPost(db: Session = Depends(get_db)):
    """
    List all blog post
    """
    all_posts = db.query(models.Blog).all()
    return all_posts

@app.get('/blog/{id}', response_model=schemas.ShowBlog)
def getIndividualPost(id, db: Session = Depends(get_db)):
    """
    Retrive individual post with a specific id
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog post with the {'title'} not available")
    return blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
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

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
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


@app.put('/user')
def createUser(request: schemas.User, db: Session = Depends(get_db)):
    """
    Creating a User 
    """
    
    new_user = models.User(name=request.name, email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user