
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session


from .. import schemas, models, database, hashing
 
router = APIRouter()

@router.post('/user', response_model=schemas.ShowUser, tags=["users"])
def createUser(request: schemas.User, db: Session = Depends(database.get_db)):
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

@router.get('/user/{id}', response_model=schemas.ShowUser, tags=["users"])
def getUser(id:int, db: Session = Depends(database.get_db)):
    """
    Retrive an individual user with a specific id
    """
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with the {'name'} not available")
    return user