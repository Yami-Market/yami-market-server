from pydantic import BaseModel


class Category(BaseModel):
    id: str
    name: str
    parent_id: str | None
    level: int


class CategoryList(BaseModel):
    items: list[Category]
