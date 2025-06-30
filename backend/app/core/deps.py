from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.core import db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


async def get_session():
    with Session(db.engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]