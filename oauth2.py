import schemas, database, models
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from datetime import datetime, timedelta, timezone

# SECRET_KEY
# ALGORITHM
# TOKEN EXPIRATION TIME

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : int(expire.timestamp())})

    encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_token

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credential_exception
        
        token_data = schemas.TokenData(id=id)
    
    except JWTError as e:
        print(e)
        raise credential_exception
    except AssertionError as e:
        print(e)

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_excpetion = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f"Could not validate credentails", headers={"WWW-Authentication" : "Bearer"})
    token = verify_access_token(token, credential_excpetion)
    user_details = db.query(models.User).filter(models.User.id == token.id).first()
    return user_details

