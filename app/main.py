from fastapi import FastAPI

from .orders.handlers import router as orders_router
from .products.handlers import router as products_router

app = FastAPI()

app.include_router(products_router, prefix="/api/v1")
app.include_router(orders_router, prefix="/api/v1")
