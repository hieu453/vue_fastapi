import time
import psycopg2
from sqlmodel import Session, select

from app.models import User


def get_user_by_email(session: Session, email: str):
    user_db = session.exec(select(User).where(User.email == email)).first()
    return user_db


def wait_for_connection(dbname: str, user: str, password: int | str, host: str, port: int):
    while True:
        try:
            conn = psycopg2.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )
            conn.close()
            break
        except psycopg2.OperationalError:
            print("PostgreSQL is not ready, waiting...")
            time.sleep(5)

    