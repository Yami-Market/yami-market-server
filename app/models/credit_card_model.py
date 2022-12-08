from pydantic import BaseModel


class CreditCard(BaseModel):
    id: str
    user_id: str
    card_type: str
    card_number: str
    card_holder_name: str
    card_expiry_month: int
    card_expiry_year: int
    cvv_code: str
    created_at: float
    updated_at: float


class CreditCardList(BaseModel):
    items: list[CreditCard]
