from datetime import datetime

from pydantic import BaseModel

from app.models.address_model import Address, BillingAddressBody


class NewCreditCardBody(BaseModel):
    card_type: str
    card_number: str
    card_holder_name: str
    card_expiry_month: str
    card_expiry_year: str
    cvv_code: str


class CreditCardBodyParams(BaseModel):
    credit_card: NewCreditCardBody
    billing_address: BillingAddressBody


class CreditCard(BaseModel):
    id: str
    user_id: str
    billing_address_id: str
    card_type: str
    card_number: str
    card_holder_name: str
    card_expiry_month: str
    card_expiry_year: str
    cvv_code: str
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }


class CreditCardWithBillingAddress(CreditCard):
    billing_address: Address

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }


class CreditCardWithBillingAddressList(BaseModel):
    items: list[CreditCardWithBillingAddress]

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }


class CreditCardList(BaseModel):
    items: list[CreditCard]

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }
