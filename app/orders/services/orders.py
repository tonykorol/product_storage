from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.orders.schemas import OrderCreateSchema
from database.models import Order, Product, OrderItem


def create_new_order(order: OrderCreateSchema, session: Session) -> Order:
    order_items = create_order_items_list(order, session)
    new_order = Order()
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    add_items_in_order(order_items, new_order, session)
    return new_order

def create_order_items_list(order: OrderCreateSchema, session: Session) -> list:
    order_items = []
    for item in order.order_items:
        product_id = item.product_id
        quantity = item.product_quantity

        product = session.query(Product).filter(Product.id == product_id).first()
        if product is None:
            raise HTTPException(status_code=404, detail=f'Product with id {product_id} not found.')

        stock_check(product, quantity)

        order_item = OrderItem(product_id=product.id, product_quantity=quantity)
        order_items.append(order_item)
    return order_items

def stock_check(product: Product, quantity: int) -> None:
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail=f'There are not enough {product.name} in stock.')
    product.stock -= quantity

def create_order(session: Session) -> Order:
    new_order = Order()
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order

def add_items_in_order(items: list, order: Order, session: Session) -> None:
    for item in items:
        item.order_id = order.id
        session.add(item)
    session.commit()
    session.refresh(order)
