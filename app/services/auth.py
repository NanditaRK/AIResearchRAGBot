from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import config
from app.db.database import get_db
from app.repositories.auth import get_user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


    
# verifies if a plain text password matches a hashed password
# returns True if passwords match, False otherwise
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# generates a hashed version of a plain text password
# returns the hashed password string
def get_password_hash(password):
    return pwd_context.hash(password)


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
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
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
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username = payload.get("sub")
        auth_method = payload.get("auth_method", "password")  # Default to password auth

        if username is None:
            raise credentials_exception

        user = get_user(username, db)
        if user is None:
            raise credentials_exception

        return {"user": user, "auth_method": auth_method}  # Return user and auth method

    except jwt.InvalidTokenError:
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

