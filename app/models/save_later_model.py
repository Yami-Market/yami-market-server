from datetime import datetime

from pydantic import BaseModel


class SaveLater(BaseModel):
    product_id: str
    user_id: str


class SaveLaterProduct(BaseModel):
    product_id: str
    name: str
    list_price: float
    image_url: str
    category_id: str
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }


class SaveLaterItemProductList(BaseModel):
    items: list[SaveLaterProduct]

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }
