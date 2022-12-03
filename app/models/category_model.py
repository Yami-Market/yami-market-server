from pydantic import BaseModel


class Category(BaseModel):
    id: str
    name: str
    parent_id: str | None
    parent_name: str | None
    level: int


class CategoryList(BaseModel):
    items: list[Category]
