from sqlalchemy import create_engine
from sqlmodel import SQLModel

db_url = "postgresql://root:123456@db:5432/fastapi"

engine = create_engine(db_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)