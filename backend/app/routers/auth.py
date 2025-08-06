from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
import jwt
from pydantic import ValidationError

from app.core.deps import SessionDep
from app.core.security import ALGORITHM, SECRET_KEY, authenticate, check_valid_refresh_token, create_access_token, create_refresh_token, get_current_user, get_hashed_password
from app.models import Token, TokenPayload, User, UserPublic, UserRegister
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
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate(session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            # samesite="strict",
            max_age=60 * 60 * 24
        )
    return Token(
        access_token=access_token,
        token_type="bearer"
    )   


@router.post("/refresh-token")
async def get_refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    access_token = check_valid_refresh_token(refresh_token)
    return {"access_token": access_token}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Logout successfully!"}
