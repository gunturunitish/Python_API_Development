from sqlalchemy.orm import Session
import models, schemas, utils, oauth2
from database import engine, SessionLocal, get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, HTTPException, Response

authentication_router = APIRouter(prefix="/authentication", tags=["Authentication"])



@authentication_router.post("/login", response_model=schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # In OAuth2PasswordRequestForm, while retreiving the details we need to use the username not the email field.
    user_details = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user_details:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user_details.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    
    # Create Token
    access_token = oauth2.create_access_token(data={"user_id" : user_details.id})
    # return Token
    return {"access_token" : access_token, "token_type": "bearer"}


# @authentication_router.post("/login")
# def login(user_credentials : schemas.UserLogin, db: Session = Depends(get_db)):

#     user_details = db.query(models.User).filter(models.User.email == user_credentials.email).first()
#     if not user_details:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="Invalid Credentials")
    
#     if not utils.verify(user_credentials.password, user_details.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="Invalid Credentials")
    
#     # Create Token
#     access_token = oauth2.create_access_token(data={"user_id" : user_details.id})
#     # return Token
#     return {"access_token" : access_token, "token_type": "bearer"}

