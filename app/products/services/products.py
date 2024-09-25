from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.products.schemas import ProductCreateSchema, ProductEditSchema
from database.models import Product


def create_new_product(product: ProductCreateSchema, session: Session ) -> Product:
    """
    Создание нового товара.

    :param product: Схема товара, содержащая необходимую информацию.
    :param session: Сессия, для взаимодействия с базой данных.
    :return: Объект созданного товара.
    """
    product_model = Product(**product.model_dump())
    session.add(product_model)
    session.commit()
    session.refresh(product_model)
    return product_model

def get_products_list(session: Session) -> list[Product]:
    """
    Получение списка всех товаров из базы данных.

    :param session: Сессия, для взаимодействия с базой данных.
    :return: Список объектов товаров.
    """
    products = session.query(Product).all()
    return products

def get_product_by_id(product_id: int, session: Session) -> Product:
    """
    Получение товара по идентификатору.

    :param product_id: Идентификатор товара.
    :param session: Сессия, для взаимодействия с базой данных.
    :return: Объект товара.
    """
    product = session.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Invalid product id")
    return product

def edit_product(product: Product, new_product_info: ProductEditSchema, session: Session) -> Product:
    """
    Изменение данных о товаре.

    :param product: Объект товара для изменения.
    :param new_product_info: Схема товара, содержащая необходимую информацию.
    :param session: Сессия, для взаимодействия с базой данных.
    :return: Объект товара.
    """
    product.name = new_product_info.name
    product.desc = new_product_info.desc
    product.price = new_product_info.price
    product.stock = new_product_info.stock
    session.commit()
    session.refresh(product)
    return product


def delete_product_by_id(product: Product, session: Session):
    """
    Удаление товара из базы данных.

    :param product: Объект товара для удаления.
    :param session: Сессия, для взаимодействия с базой данных.
    """
    session.delete(product)
    session.commit()
