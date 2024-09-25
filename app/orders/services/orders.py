from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.orders.schemas import OrderCreateSchema
from database.models import Order, Product, OrderItem, Status


def create_new_order(order: OrderCreateSchema, session: Session) -> Order:
    """
    Создание нового заказа.

    :param order: Схема заказа, содержащая информацию о товаре и количестве.
    :param session: Сессия для взаимодействия с базой данных.
    :return: Созданный объект заказа.
    """
    order_items = create_order_items_list(order, session)
    new_order = Order()
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    add_items_in_order(order_items, new_order, session)
    return new_order

def create_order_items_list(order: OrderCreateSchema, session: Session) -> list:
    """
    Создание списка элементов заказа.

    :param order: Схема заказа, содержащая информацию о товаре и количестве.
    :param session: Сессия для взаимодействия с базой данных.
    :return: Список с элементами заказа
    """
    order_items = []
    for item in order.order_items:
        product_id = item.product_id
        quantity = item.product_quantity

        product = session.query(Product).filter(Product.id == product_id).first()
        if product is None:
            raise HTTPException(status_code=404, detail=f'Product with id {product_id} not found.')

        stock_check(product, quantity)

        price = round(product.price * quantity, 2)

        order_item = OrderItem(product_id=product.id, product_quantity=quantity, price=price)
        order_items.append(order_item)
    return order_items

def stock_check(product: Product, quantity: int) -> None:
    """
    Проверка наличия товара на складе и обновление его количества.

    :param product: Объект товара для проверки.
    :param quantity: Количество товара для заказа.
    """
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail=f'There are not enough {product.name} in stock.')
    product.stock -= quantity

def add_items_in_order(items: list[OrderItem], order: Order, session: Session) -> None:
    """
    Добавление элементов заказа в заказ и обновление суммы заказа.

    :param items: Список элементов заказа.
    :param order: Объект заказа.
    :param session: Сессия для взаимодействия с базой данных.
    """
    price = 0
    for item in items:
        item.order_id = order.id
        price += item.price
        session.add(item)
    order.price = round(price, 2)
    session.commit()
    session.refresh(order)

def get_orders_list(session: Session) -> list[Order]:
    """
    Получение списка всех заказов из базы данных.

    :param session: Сессия для взаимодействия с базой данных.
    :return: Список объектов всех заказов.
    """
    orders = session.query(Order).all()
    return orders

def get_order(order_id: int, session: Session) -> Order:
    """
    Получение заказа по идентификатору.

    :param order_id: Идентификатор заказа.
    :param session: Сессия для взаимодействия с базой данных.
    :return: Объект заказа.
    """
    order = session.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Invalid order id")
    return order

def update_status(order: Order, status_id: int, session: Session) -> Order:
    """
    Обновление статуса заказа.

    :param order: Объект заказа для обновления статуса.
    :param status_id: Идентификатор статуса.
    :param session: Сессия, для взаимодействия с базой данных.
    :return: Объект заказа.
    """
    status = session.query(Status).filter(Status.id == status_id).first()
    if status is None:
        raise HTTPException(status_code=404, detail="Invalid status")
    order.status = status
    session.commit()
    return order