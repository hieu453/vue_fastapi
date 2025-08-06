import math
from fastapi import APIRouter, HTTPException
from fastapi import status
from sqlalchemy import delete
from sqlmodel import select
from sqlalchemy import func

from app.core.deps import SessionDep
from app.models import Product, ProductCreate, ProductUpdate

router = APIRouter()

@router.get("/products")
async def read_products(session: SessionDep, limit: int = 10, page: int = 1):
    total_products = session.exec(select(func.count(Product.id)).select_from(Product)).one() # type: ignore
    pages = math.ceil(total_products / limit)
    if page > pages:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
            )
    offset = (page - 1) * limit
    products = session.exec(select(Product).offset(offset).limit(limit)).all()
    return {
            "products": products,
            "total_products": total_products,
            "total_products_per_page": limit,
            "total_pages": pages,
        }


@router.get("/test")
async def test(session: SessionDep):
    num_products = session.exec(select(func.count(Product.id)).select_from(Product)) # type: ignore
    return num_products


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

