from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import db
from app.routers import products, users

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db.create_db_and_tables()

app.include_router(products.router, tags=["Products"], prefix="/api")
app.include_router(users.router, tags=["Users"], prefix="/api")


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
