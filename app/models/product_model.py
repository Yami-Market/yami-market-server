from pydantic import BaseModel


class Product(BaseModel):
    id: str
    name: str
    unit_price: float
    image_url: str
    # FIXME: change to category id later
    third_category_id: str
