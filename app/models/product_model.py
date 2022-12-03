from pydantic import BaseModel


class Product(BaseModel):
    id: str
    name: str
    list_price: float
    image_url: str
    category_id: str


class ProductList(BaseModel):
    items: list[Product]
