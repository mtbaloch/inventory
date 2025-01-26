from fastapi import APIRouter, Form, Response, status, Depends, HTTPException
from app.core.db import db_session
from app.models.user import User
from sqlmodel import Session, select
from app.api.utils.user_auth_utils import Auth
from app.api.utils.user_auth_utils import get_user_auth

user_router = APIRouter(prefix='/users', tags=["Users"])


@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_new_user(user_data: User, user_auth: Auth = Depends(get_user_auth) ):

    if not user_data.first_name or not user_data.user_name or not user_data.email or not user_data.last_name  or not user_data.password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="All feilds are required.")
    
    # is user_name already used
    
    user_by_user_name = await user_auth.get_user_by_user_name(user_data.user_name)
    
    if user_by_user_name:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already used, try with unique name")
    
    # email validation through get_user_by_email method
    user = await user_auth.get_user_by_email(user_data.email)
   
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user with this email already exist.")
    print(f"user with common password : {user_data}")
    # hashed password
    hashed_password = user_auth.hash_password(user_data.password)
    user_data.password = hashed_password
    
    print(f"user with hashed password : {user_data}")
    
    user_auth.db_session.add(user_data)
    user_auth.db_session.commit()
    user_auth.db_session.refresh(user_data)
    
    if user_data is None:
        raise HTTPException(status=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error")
    
    return {"status":True, "message":"User created successfully", "user": user_data}
    

@user_router.post("/signin")
async def signin_user(response: Response, user_email: str = Form(...), user_password: str = Form(...), user_auth: Auth = Depends(get_user_auth)):
    is_user_exist = await user_auth.get_user_by_email(user_email)
    
    if not is_user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this email not exist")
    
    is_password_match = user_auth.verify_password(user_password,is_user_exist.password)

    if not is_password_match:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials")
    
    user_id = str(is_user_exist.id)
    
    access_token, refresh_token = user_auth.create_tokens(user_id)
    
    response.set_cookie(
        key="inventory_refresh_token",
        value = refresh_token,
        httponly=False,
        secure=True,
        samesite="strict"
    )
    return {
        "status":True,
        "message":"you are logged in successfully",
        "access_token":access_token,
        "user": is_user_exist
    }
        