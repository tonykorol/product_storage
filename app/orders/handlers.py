from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.orders.schemas import OrderSchema, OrderCreateSchema
from app.orders.services.orders import create_new_order
from database.database import get_session

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderSchema)
def create_order(
        order_items: OrderCreateSchema,
        session: Session = Depends(get_session)
):
    new_order = create_new_order(order_items, session)
    return new_order


