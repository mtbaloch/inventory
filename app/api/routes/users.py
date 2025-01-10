from fastapi import APIRouter, status, Depends, HTTPException
from app.core.db import db_session
from app.models.users import User
from sqlmodel import Session, select

user_router = APIRouter(prefix='/users', tags=["users"])

@user_router.post("", status_code=status.HTTP_201_CREATED)
async def create_new_user(user_data: User, session: Session = Depends(db_session) ):

    if not user_data.first_name or not user_data.user_name or not user_data.email or not user_data.last_name  or not user_data.password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="All feilds are required.")
    
    # is user_name already used
    
    statement = select(User).where(User.user_name == user_data.user_name)
    is_user_name_exist = session.exec(statement).first() # Ture or False
    
    if is_user_name_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already used, try with unique name")
    
    # email validation
    statement = select(User).where(User.email == user_data.email)
    is_email_already_exist = session.exec(statement).first()
        
    if is_email_already_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user with this email already exist.")
    
    
    data = user_data
    
    session.add(data)
    session.commit()
    session.refresh(data)
    if data is None:
        raise HTTPException(status=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error")
    
    return {"status":True, "message":"User created successfully", "user": data}
    
