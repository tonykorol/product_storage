from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.orders.schemas import OrderSchema, OrderCreateSchema, OrderListSchema
from app.orders.services.orders import create_new_order, get_orders_list, get_order, update_status
from database.database import get_session

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderSchema)
def create_order(
        order_items: OrderCreateSchema,
        session: Session = Depends(get_session)
):
    new_order = create_new_order(order_items, session)
    return new_order

@router.get("", response_model=OrderListSchema)
def get_all_orders(
        session: Session = Depends(get_session)
):
    orders = get_orders_list(session)
    return {"orders": orders}

@router.get("/{order_id}", response_model=OrderSchema)
def get_order_by_id(
        order_id: int,
        session: Session = Depends(get_session)
):
    return get_order(order_id, session)

@router.patch("/{order_id}/status", response_model=OrderSchema)
def update_order_status(
        order_id: int,
        status_id: int,
        session: Session = Depends(get_session)
):
    order = get_order(order_id, session)
    return update_status(order, status_id, session)
