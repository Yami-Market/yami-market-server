from datetime import datetime

from pydantic import BaseModel

from app.models.address_model import Address
from app.models.credit_card_model import CreditCard
from app.models.product_model import Product


class Order(BaseModel):
    id: str
    order_date: datetime
    ship_date: datetime | None
    payment_date: datetime
    shipping_fee: float
    tax_rate: float
    user_id: str
    credit_card_id: str
    shipping_address_id: str

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }


class OrderProduct(Product):
    order_id: str
    unit_price: float
    order_quantity: int


class OrderProductDetail(Order):
    subtotal_price: float
    products: list[OrderProduct]
    shipping_address: Address
    credit_card: CreditCard

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }


class OrderProductDetailList(BaseModel):
    items: list[OrderProductDetail]

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }


class NewOrderProduct(BaseModel):
    product_id: str
    name: str
    list_price: float
    image_url: str
    category_id: str
    quantity: int


class NewOrderBodyParams(BaseModel):
    shipping_address_id: str
    credit_card_id: str
    shipping_fee: float
    products: list[NewOrderProduct]
