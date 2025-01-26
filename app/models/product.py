from sqlmodel import Field, Relationship
from app.models.common import BaseModel
from typing import Optional
import uuid

class Product(BaseModel, table=True):
    __tablename__ = "products"
    sku_number: int
    product_name: str
    description: str
    product_category: Optional[str]
    price: float
    quantity: int
    status: Optional[str] = Field(default="active")
    
    user_id: uuid.UUID = Field(foreign_key="users.id")
    
    # Relationship to User, deferred import
    user: "User" = Relationship(back_populates="products")