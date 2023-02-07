
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from .. import schemas, models, database, hashing
 
router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post('/', response_model=schemas.ShowUser)
def createUser(request: schemas.User, db: Session = Depends(database.get_db)):
    """
    Creating a User 
    """
    ## lets hash the password coming from the user
    #hashed_password = pwd_context.hash(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.get_password_hash(request.password)).first()
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.ShowUser)
def getUser(id:int, db: Session = Depends(database.get_db)):
    """
    Retrive an individual user with a specific id
    """
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with the {'name'} not available")
    return user