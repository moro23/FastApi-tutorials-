from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session


from .. import schemas, models, database

from ..oauth import get_current_user
 
router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)

@router.get('/', response_model=List[schemas.ShowBlog])
def getAllBlogPost(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user) ):
    """
    List all blog post
    """
    all_posts = db.query(models.Blog).all()
    return all_posts

@router.post('/', status_code=status.HTTP_201_CREATED)
def createBlog(request: schemas.Blog, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    """
    Creating blog post
    """
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/{id}', response_model=schemas.ShowBlog)
def getIndividualPost(id, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    """
    Retrive individual post with a specific id
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog post with the {'title'} not available")
    return blog

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
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

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def updatePost(id, request: schemas.Blog, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
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
