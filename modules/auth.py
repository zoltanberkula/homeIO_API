from datetime import datetime, timedelta
from re import S
from typing import Annotated
import jwt
from jwt import PyJWTError

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from db import authenticate_user

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

SECRET_KEY ="secretkey"
ALGORITHM = "HS256"
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/token')

class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(username: str, userID: int, expires_delta: timedelta):
    encode = {"sub": username, "id": userID}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def login_for_access_token(user: dict):
    print(user)
    if not authenticate_user(user):
        raise Exception
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    token = create_access_token(user["username"], user["password"], timedelta(minutes=20))
    print("TOKEN", token)
    return {"accessToken": token, "tokenType": "bearer"}

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    print("get_current_user",token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        print("username", username)
        print("user_id", user_id)
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return {"username": username, "id": user_id}
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")


user = {
    "username": "Zolko1995",
    "password": "Nissan350"
}
# print(login_for_access_token(user))
# print(get_current_user(str(login_for_access_token(user))))
# print(oauth2_bearer)
# print(get_current_user("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJab2xrbzE5OTUiLCJpZCI6Ik5pc3NhbjM1MCIsImV4cCI6MTcwMzAyNDU3NX0.91wflzgvwchQ3-VbbwyH8BMFJa7xcfCAJnDpByp-gTw"))