from datetime import datetime, UTC

from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    desc: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer)

    order_items: Mapped["OrderItem"] = relationship(back_populates="product")



class Status(Base):
    __tablename__ = "statuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)

    orders: Mapped["Order"] = relationship(back_populates="status")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
    price: Mapped[float] = mapped_column(Float, nullable=True)

    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"), default=1)
    status: Mapped["Status"] = relationship(back_populates="orders", lazy="joined")

    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="order", lazy="joined")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float, nullable=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product: Mapped["Product"] = relationship(back_populates="order_items")

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    order: Mapped["Order"] = relationship(back_populates="order_items")
