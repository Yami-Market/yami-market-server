from pydantic import BaseModel


class Category(BaseModel):
    id: str
    name: str
    parent_id: str | None
    parent_name: str | None
    level: int


class CategoryList(BaseModel):
    items: list[Category]


class ProductAllCategory(BaseModel):
    level_1_id: str
    level_1_name: str
    level_2_id: str
    level_2_name: str
    level_3_id: str
    level_3_name: str


class ProductAllCategoryList(BaseModel):
    items: list[ProductAllCategory]


class CategoryPath(BaseModel):
    id: str
    name: str
    parent_id: str | None
    parent_name: str | None
    grandparent_id: str | None
    grandparent_name: str | None
    level: int
