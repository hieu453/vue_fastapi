from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status

from app.core.deps import SessionDep
from app.core.security import authenticate, create_access_token, get_current_user, get_hashed_password
from app.models import Token, User, UserPublic, UserRegister
from app.utils import get_user_by_email


router = APIRouter()


@router.get("/me", response_model=UserPublic)
async def read_me(me: Annotated[UserPublic, Depends(get_current_user)]):
    return me


@router.post("/register", response_model=UserPublic)
async def register_user(session: SessionDep, user: UserRegister):
    user_db = get_user_by_email(session, user.email)
    if user_db:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    
    validated_user = User.model_validate(user, update={
        "hashed_password": get_hashed_password(user.password)
    })

    session.add(validated_user)
    session.commit()
    session.refresh(validated_user)
    return validated_user


@router.post("/token")
async def login_for_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate(session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
