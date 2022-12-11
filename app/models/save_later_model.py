from pydantic import BaseModel


class SaveLaterItem(BaseModel):
    user_id: str
    product_id: str


class SaveLaterItemList(BaseModel):
    items: list[SaveLaterItem]
