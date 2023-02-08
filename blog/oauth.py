from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from . import jwt_tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")




async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    ## import token verification
    
    return jwt_tokens.verify_token(token, credentials_exception)
    
    
 