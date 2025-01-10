from sqlmodel import Field
from app.models.common import BaseModel
from typing import Optional

class Product(BaseModel, table=True):
    __tablename__ = "products"
    sku_number: int
    product_name: str
    description: str
    product_category: Optional[str]
    price: float
    quantity: int
    status: Optional[str] = Field(default="active")
    