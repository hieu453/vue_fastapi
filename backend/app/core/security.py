from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException
import jwt
from passlib.context import CryptContext
from fastapi import status
from pydantic import ValidationError
from sqlmodel import Session, select

from app.core.deps import SessionDep, TokenDep
from app.models import Token, TokenPayload, User
from app.utils import get_user_by_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "e100dd4e54a4949a32d648cf49df93a046383a3e8e0eedabb0891276dd4e2ae8"
ALGORITHM = "HS256"


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def authenticate(session: Session, email: str, password: str):
    user_db = get_user_by_email(session=session, email=email)
    if not user_db:
        return False
    if not verify_password(password, user_db.hashed_password):
        return False
    return user_db


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(seconds=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(session: SessionDep, token: TokenDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise credentials_exception
    user = session.exec(select(User).where(User.email == token_data.sub)).first()
    if user is None:
        raise credentials_exception
    return user


def check_valid_refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        access_token = create_access_token(payload)
        return access_token
    except (jwt.InvalidTokenError, ValidationError):
        return False


CurrentUser = Annotated[User, Depends(get_current_user)]
