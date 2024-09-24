from pydantic import BaseModel, Field


class ProductCreateSchema(BaseModel):
    name: str
    desc: str
    price: float = Field(..., ge=0)
    stock: int = Field(..., ge=0)


class ProductEditSchema(ProductCreateSchema):
    pass


class ProductShowSchema(ProductCreateSchema):
    id: int


class ProductListSchema(BaseModel):
    products: list[ProductShowSchema]
