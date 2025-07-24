from fastapi import APIRouter, HTTPException
from sqlalchemy import delete
from sqlmodel import select

from app.core.deps import SessionDep
from app.models import Product, ProductCreate, ProductUpdate

router = APIRouter()


@router.get("/products", response_model=list[Product])
async def read_products(session: SessionDep, limit: int = 10, offset: int = 0):
    products = session.exec(select(Product).offset(offset).limit(limit)).all()
    return products


@router.get("/products/{product_id}", response_model=Product)
async def read_one_product(session: SessionDep, product_id: int):
    product = session.exec(select(Product).where(Product.id == product_id)).first()
    return product


@router.post("/products", response_model=Product)
async def create_product(session: SessionDep, product: ProductCreate):
    validated_product = Product.model_validate(product)
    session.add(validated_product)
    session.commit()
    session.refresh(validated_product)
    return validated_product


@router.patch("/products/{product_id}", response_model=Product)
async def patch_product(product_id: int, session: SessionDep, product: ProductUpdate):
    product_db = session.get(Product, product_id)
    if not product_db:
        raise HTTPException(
            status_code=404,
            detail="product not found"
        )
    product_data = product.model_dump(exclude_unset=True)
    product_db.sqlmodel_update(product_data)
    session.add(product_db)
    session.commit()
    session.refresh(product_db)
    return product_db


@router.delete("/products/{product_id}/delete")
async def delete_product(product_id: int, session: SessionDep):
    product_db = session.get(Product, product_id)
    if not product_db:
        raise HTTPException(
            status_code=404,
            detail="product not found"
        )
    session.delete(product_db)
    session.commit()
    return {"message": "Product(s) deleted"}


@router.delete("/products/{product_ids}/delete-ids")
async def delete_products(product_ids: str, session: SessionDep):
    product_ids = eval(product_ids)
    if isinstance(product_ids, int):
        session.exec(delete(Product).where(Product.id == product_ids)) # type: ignore
    if isinstance(product_ids, tuple):
        session.exec(delete(Product).where(Product.id.in_(product_ids))) # type: ignore
    session.commit()
    return {"message": "Products deleted"}

