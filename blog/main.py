from fastapi import FastAPI, Depends
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


@app.post('/blog')
def createBlog(request: schemas.Blog, db: Session = Depends(get_db)):
    """
    Creating blog post
    """
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
def getAllBlogPost(db: Session = Depends(get_db)):
    """
    List all blog post
    """
    all_posts = db.query(models.Blog).all()
    return all_posts

@app.get('/blog/{id}')
def getIndividualPost(id,db: Session = Depends(get_db)):
    """
    Retrive individual post with a specific id
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog