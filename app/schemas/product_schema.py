from sqlmodel import SQLModel
from typing import Optional

class productSchema(SQLModel):
    sku_number: int
    product_name: str
    description: str
    product_category: Optional[str]
    price: float
    quantity: int

    class Config:
        orm_mode=True