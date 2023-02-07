from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from .. import schemas, database, models

from ..hashing import Hash

from .. import jwt_tokens

router = APIRouter(
    tags=['Login']
)


@router.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with the {user} not available")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=404, detail=f"Credentials does not match?")
    
    ## generate a jwt access token
    access_token = jwt_tokens.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
    #return user