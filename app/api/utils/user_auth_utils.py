import jwt
from sqlmodel import Session, select
from fastapi import Depends
from app.core.db import db_session
from typing import Union
from app.models.users import User
import bcrypt
from datetime import datetime, timezone, timedelta

class Auth:
    # constant
    access_token_key= "ndng93838490i93r9nre340"
    refresh_token_key="eriofgj390u490r338u4ur934u0r93u"
    def __init__(self, db_session: Session = Depends(db_session)):
        self.db_session = db_session
    
    async def get_user_by_email(self, email:str)-> Union[User, None]:
        # transformation of specific data to run validations
        # transformation is type casting, data operations
        # mtbaloch666@gmail.com 
        print("email in class method", email)
        email_in_lowercase = email.lower()
        statement = select(User).where(User.email == email_in_lowercase)
        # true or false but it depends on returning data
        # {id, last_name, first_name, password}
        user = self.db_session.exec(statement).first()
        # either user will be or not
        print(user)
        return user
    
    async def get_user_by_id(self, id:str)-> Union[User, None]:
        user_id = id
        statement = select(User).where(User.id == user_id)
        # true or false but it depends on returning data
        # {id, last_name, first_name, password}
        user = self.db_session.exec(statement).first()
        # either user will be or not
        return user

    async def get_user_by_user_name(self, user_name: str)-> Union[User, None]:
         statement = select(User).where(User.user_name == user_name)
         user = self.db_session.exec(statement).first() # Ture or False
         return user
    
    # Static Method
    @staticmethod
    def hash_password(password: str) -> str:
        # use bcrypt to hash password
        # saltvalue = 10 
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
    # independent of class attributes or methods
    
    @staticmethod
    def verify_password(password:str, hashed_password: str) -> bool:
        is_password_match = bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        return is_password_match

    # assumptions
    # programmer or developer must write assumptions before writing code
    # create tokens 
    # access_token, refresh_token
    # user_id
    # create access-token and referesh_token with jwt
    # expiry date
    # issue date
    # return two things access token and refresh token tuple
    
    def create_tokens(self, user_id: str) -> tuple[str, str]:
        # issue date
        issued_at = datetime.now(timezone.utc)
        # expirt date
        access_token_expire_at = datetime.now(timezone.utc) + timedelta(hours=3)
        refresh_token_expire_at = datetime.now(timezone.utc) + timedelta(days=7)
        # create access token
        access_token = jwt.encode(
            {"sub": user_id, "exp": access_token_expire_at, "iat": issued_at},
            self.access_token_key,
            algorithm="HS256"
            
        )
        # create refresh token
        refresh_token = jwt.encode(
            {"sub": user_id, "exp": refresh_token_expire_at, "iat": issued_at},
            self.refresh_token_key,
            algorithm="HS256"
            
        )
        
        return access_token, refresh_token
        
# userAuth = Auth() # constructor function


# is class is callable/invoke = yes
# object itself is not callable/invokeable 