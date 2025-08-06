from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://root:123456@db:5432/fastapi"
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()
