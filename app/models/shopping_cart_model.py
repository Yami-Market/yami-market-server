from pydantic import BaseModel, validator


def quantity_can_not_less_than_one(cls, v: int):
    if v < 1:
        raise ValueError('Quantity must be greater than 0')
    return v


class ShoppingCartPostBodyItem(BaseModel):
    product_id: str
    quantity: int

    _quantity_validator = validator(
        'quantity', allow_reuse=True)(quantity_can_not_less_than_one)


class ShoppingCartPostBodyParams(BaseModel):
    items: list[ShoppingCartPostBodyItem]


class ShoppingCartPutBodyParams(BaseModel):
    quantity: int

    _quantity_validator = validator(
        'quantity', allow_reuse=True)(quantity_can_not_less_than_one)


class ShoppingCartItem(BaseModel):
    user_id: str
    product_id: str
    quantity: int


class ShoppingCartItemList(BaseModel):
    items: list[ShoppingCartItem]
