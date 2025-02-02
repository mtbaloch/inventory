from fastapi import HTTPException, Request, status
from app.api.utils.user_auth_utils import Auth

# create a middleware funtion
def auth(request: Request):
    # inside request, we have authorization token
    # we add authorization header explicitly in request from frontend
    # auth_header type will be string
    auth_header = request.headers.get("Authorization") 
    # validate, whether auth_header is available or not
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Auth token missing or invalid")
    
    "[Bearer, eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzZmE4NWY2NC01NzE3LTQ1NjItYjNmYy0yYzk2M2Y2NmFmYTYiLCJleHAiOjE3Mzc5MjIwNjMsImlhdCI6MTczNzkxMTI2M30.u8mZGQwUkGYkaNQOpFD9kybd5iaY9M7h1AmW7s1-IMM]"

    token = auth_header.split(" ")[1]

    auth = Auth()

    decoded_token = auth.verify_token(token)

    if not decoded_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid or expired token")
    
    user_id = decoded_token.get("sub")
    
    return user_id

