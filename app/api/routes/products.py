from fastapi import APIRouter, Depends, Header, status, HTTPException
from app.core.db import db_session
from app.models.product import Product
from app.schemas.product_schema import productSchema
from sqlmodel import Session, select
from typing import Optional
from app.api.middlewares.auth_middleware import auth

product_router = APIRouter(prefix="/products", tags=["products"])

@product_router.post("/")
async def create_new_product(product_data:productSchema, user_id: str = Depends(auth),db: Session = Depends(db_session)):
   
    if not product_data.description or not product_data.price or not product_data.product_name or not product_data.product_category or not product_data.quantity:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="All fields are required")
    # Handle the invalid data case
        

    # we accept the user_id from auth middleware which is coming after 
    # verifying the identity of user/customer
    # as we are validating our body data on the basis
    # of schema model which is not for database tables
    # therefore, we need to first dumpt the incoming data
    # into pyhton dictionary using model_dump() method
    data = product_data.model_dump()
    data["user_id"] = user_id
    # after that we use main Product model to create data 
    # that we use to save in database
    # ** mean destructure the dictionary items
    data = Product(**data)
    # below we will send data to the table
    db.add(data)
    db.commit()
    db.refresh(data)
    
    return {"status":True, "message":"Product is created successfully", "data":data}



@product_router.get("/")
async def get_all_products(auth = Depends(auth), db: Session = Depends(db_session)):
    
    statement = select(Product)
    products =  db.exec(statement).all()

    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product found")

    return {"status":True, "message":"products fetched successfully", "data": products}



# create endpoint to get signle product




# create endpoint to get products of any single user