from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.orm import Session

from app import config
from app.db.database import get_db
from app.db.models import User
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.services.auth import authenticate_user, create_access_token, get_current_active_user

router = APIRouter()

@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


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
    access_token_expires = timedelta(minutes=int(config.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}