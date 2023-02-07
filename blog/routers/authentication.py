from fastapi import APIRouter, Depends, HTTPException

from .. import schemas, database, models

from ..hashing import Hash

from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Login']
)


@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with the {user} not available")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=404, detail=f"Credentials does not match?")
    
    ## generate a jwt token
    return user