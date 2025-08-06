from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import products
from app.routers import auth
from app.core.security import get_current_user
from app.utils import wait_for_connection

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

wait_for_connection("fastapi", "root", 123456, "db", 5432)


app.include_router(products.router, tags=["Products"], prefix="/api")
# app.include_router(products.router, tags=["Products"], prefix="/api", dependencies=[Depends(get_current_user)])
app.include_router(auth.router, tags=["Users"], prefix="/api")


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
