from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.products.schemas import ProductCreateSchema, ProductEditSchema
from database.models import Product


def create_new_product(product: ProductCreateSchema, session: Session ) -> Product:
    product_model = Product(**product.model_dump())
    session.add(product_model)
    session.commit()
    session.refresh(product_model)
    return product_model

def get_products_list(session: Session) -> list[Product]:
    products = session.query(Product).all()
    return products

def get_product_by_id(product_id: int, session: Session) -> Product:
    product = session.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Invalid product id")
    return product

def edit_product(product: Product, new_product_info: ProductEditSchema, session: Session) -> Product:
    product.name = new_product_info.name
    product.desc = new_product_info.desc
    product.price = new_product_info.price
    product.stock = new_product_info.stock
    session.commit()
    session.refresh(product)
    return product


def delete_product_by_id(product: Product, session: Session):
    session.delete(product)
    session.commit()
