from datetime import datetime

from pydantic import BaseModel


class Order(BaseModel):
    id: str
    order_date: datetime | None
    ship_date: datetime | None
    payment_date: datetime | None
    shipping_fee: float
    tax_rate: float
    user_id: str
    credit_card_id: str
    shipping_address_id: str


class OrderItem(BaseModel):
    order_id: str
    product_id: str
    quantity: int


class NEW_ORDER(BaseModel):
    shipping_fee: float
    tax_rate: float
    credit_card_id: str
    shipping_address_id: str
