from fastapi import APIRouter, Depends, Header, status, HTTPException
from app.core.db import db_session
from app.models.product import Product
from app.api.utils.user_auth_utils import get_user_auth
from sqlmodel import Session, select
from typing import Optional
product_router = APIRouter(prefix="/products", tags=["products"])

@product_router.post("/")
async def create_new_product(product_data:Product, authorization:str = Header(...),db: Session = Depends(db_session), session:Session = Depends(get_user_auth)):
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unathorized to create new product")
    
    "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzZmE4NWY2NC01NzE3LTQ1NjItYjNmYy0yYzk2M2Y2NmFmYTYiLCJleHAiOjE3Mzc5MjIwNjMsImlhdCI6MTczNzkxMTI2M30.u8mZGQwUkGYkaNQOpFD9kybd5iaY9M7h1AmW7s1-IMM"
    token = authorization.split(" ")[1]

    isTokenVerified = session.verify_token(token)
    print(isTokenVerified)

    if not isTokenVerified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"token error {isTokenVerified}")
    
    user_id = isTokenVerified["sub"]

    if not product_data.description or not product_data.price or not product_data.status or not product_data.user_id or not product_data.updated_at or not product_data.created_at or not product_data.product_name or not product_data.product_category or not product_data.quantity:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="All fields are required")
    # Handle the invalid data case
        


    product_data.user_id= user_id

    db.add(product_data)
    db.commit()
    db.refresh(product_data)
    
    return {"status":True, "message":"Product is created successfully", "data":product_data}



@product_router.get("/")
async def get_all_products(authorization:Optional[str] = Header(None), db: Session = Depends(db_session)):


    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    statement = select(Product)
    products =  db.exec(statement).all()

    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product found")

    return {"status":True, "message":"products fetched successfully", "data": products}



# create endpoint to get signle product




# create endpoint to get products of any single user