from datetime import datetime

from pydantic import BaseModel


class Address(BaseModel):
    id: str
    user_id: str
    first_name: str
    last_name: str
    street_address: str
    optional_address: str | None
    city: str
    state: str
    country: str
    zip_code: str
    phone_number: str
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }


class AddressList(BaseModel):
    items: list[Address]

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }


class AddressBodyParams(BaseModel):
    first_name: str
    last_name: str
    street_address: str
    optional_address: str | None
    city: str
    state: str
    country: str
    zip_code: str
    phone_number: str
    email: str


class BillingAddressBody(BaseModel):
    id: str | None
    user_id: str | None
    first_name: str
    last_name: str
    street_address: str
    optional_address: str | None
    city: str
    state: str
    country: str
    zip_code: str
    phone_number: str
    email: str
