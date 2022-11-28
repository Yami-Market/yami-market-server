from pydantic import BaseModel, validator


class ShoppingCartBodyParams(BaseModel):
    quantity: int

    @validator('quantity')
    def quantity_can_not_less_than_one(cls, v: int):
        if v < 1:
            raise ValueError('Quantity must be greater than 0')
        return v


class ShoppingCartItem(BaseModel):
    user_id: str
    product_id: str
    quantity: int


class ShoppingCartItemList(BaseModel):
    items: list[ShoppingCartItem]
