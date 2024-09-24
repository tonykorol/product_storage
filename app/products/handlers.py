from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.products.schemas import ProductCreateSchema, ProductShowSchema, ProductListSchema, ProductEditSchema
from app.products.services.products import create_new_product, get_products_list, get_product_by_id, edit_product, \
    delete_product_by_id
from database.database import get_session

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("", response_model=ProductShowSchema)
def create_product(product: ProductCreateSchema, session: Session = Depends(get_session)):
    """
    Create new product.
    """
    try:
        return create_new_product(product, session)
    except IntegrityError:
        raise HTTPException(status_code=422, detail="Product already exists")

@router.get("", response_model=ProductListSchema)
def get_all_products(session: Session = Depends(get_session)):
    """Get all products."""
    products = get_products_list(session)
    return {"products": products}

@router.get("/{product_id}", response_model=ProductShowSchema)
def get_product_info(product_id: int, session: Session = Depends(get_session)):
    """Get product info by id."""
    return get_product_by_id(product_id, session)

@router.put("/{product_id}", response_model=ProductShowSchema)
def edit_product_info(
        product_id: int,
        new_product_info: ProductEditSchema,
        session: Session = Depends(get_session)):
    """Edit product info."""
    product = get_product_by_id(product_id, session)
    return edit_product(product, new_product_info, session)

@router.delete("/{product_id}")
def delete_product(
        product_id: int,
        session: Session = Depends(get_session)
):
    """Delete product."""
    product = get_product_by_id(product_id, session)
    delete_product_by_id(product, session)
    return {"message": f"Product {product_id} successfully deleted."}
