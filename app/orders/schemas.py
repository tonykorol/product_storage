from datetime import datetime

from pydantic import BaseModel


class StatusSchema(BaseModel):
    id: int
    name: str

class OrderItemCreateSchema(BaseModel):
    product_id: int
    product_quantity: int

class OrderItemShowSchema(OrderItemCreateSchema):
    price: float

class OrderCreateSchema(BaseModel):
    order_items: list[OrderItemCreateSchema]

class OrderSchema(BaseModel):
    id: int
    created_at: datetime
    status: StatusSchema
    price: float
    order_items: list[OrderItemShowSchema]

class OrderListSchema(BaseModel):
    orders: list[OrderSchema]
