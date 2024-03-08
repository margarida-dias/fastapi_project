from typing import Optional

from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    url: str
    user_id: Optional[int] = None

    class Config:
        orm_mode = True
