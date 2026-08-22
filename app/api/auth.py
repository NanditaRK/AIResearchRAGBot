from typing import Annotated
import os
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.schemas import UsrInDB
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta,timezone

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_user(email: str, password: str, full_name: str, db: Session):
    hashed_password = get_password_hash(password)
    new_user = User(email=email,
    hashed_password=hashed_password,
    full_name=full_name,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
    
# verifies if a plain text password matches a hashed password
# returns True if passwords match, False otherwise
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# generates a hashed version of a plain text password
# returns the hashed password string
def get_password_hash(password):
    return pwd_context.hash(password)

# retrieves a user from the database by username
# returns a UsrInDB object if found, None otherwise
def get_user(email: str, db: Session):
    
    user: UsrInDB = db.get(User, {"email": email})
    
    return user

# authenticates a user by verifying username and password
# returns the user object if authentication successful, False otherwise
def  authenticate_user( email: str, password: str, db: Session):
    user = get_user(email, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# this function is used to create access token
# it takes in settings, data, expires_delta and auth_method as arguments
# returns the encoded jwt token
def create_access_token(data: dict, expires_delta: timedelta | None = None, auth_method="password"):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire, "auth_method": auth_method})  # Include auth method
    encoded_jwt = jwt.encode(to_encode, os.environ["SECRET_KEY"], algorithm=os.environ["ALGORITHM"])
    return encoded_jwt

# verifies the token and returns the user and auth method
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=[os.environ["ALGORITHM"]])
        username = payload.get("sub")
        auth_method = payload.get("auth_method", "password")  # Default to password auth

        if username is None:
            raise credentials_exception

        user = get_user(username, db)
        if user is None:
            raise credentials_exception

        return {"user": user, "auth_method": auth_method}  # Return user and auth method

    except InvalidTokenError:
        raise credentials_exception

# verifies if a user is active (not disabled)
# raises HTTPException if user is disabled otherwise returns the user
async def get_current_active_user(
    current_user_data: Annotated[dict, Depends(get_current_user)]
):
    user = current_user_data["user"]
    auth_method = current_user_data["auth_method"]

    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return {"user": user, "auth_method": auth_method}


# endpoint for user authentication and token generation
# validates username/password and returns JWT access token if valid
@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user( form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}