from sqlmodel import Session, select

from app.models import User


def get_user_by_email(session: Session, email: str):
    user_db = session.exec(select(User).where(User.email == email)).first()
    return user_db    