from curses.ascii import HT
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import jwt
from passlib.hash import bcrypt
from tortoise.contrib.fastapi import register_tortoise

#from models import User, User_Pydantic, UserIn_Pydantic, oauth2_scheme
from db import insertRecord, getTableContent, reg_user, login_user

from auth import login_for_access_token, get_current_user
from utils import credentials as creds

from publishAWS import onOFF, sendCMD, sendRQST, deviceON, deviceOFF

app = FastAPI()

#dbInit()

origins = [creds["fast_api_origin_addr"],]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"]
)

    
@app.post('/token')
async def generate_token(user: dict):
    return login_for_access_token(user)

@app.post('/register')
async def create_user(user: dict): #type: ignore
    #print(user)
    return await reg_user(user)

@app.post('/login')
async def login(user: dict): #type: ignore
    #print(user)
    return await login_user(user)

user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get('/me', status_code=status.HTTP_200_OK)
async def user(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed.")
    return {"User": user}

@app.get('/gettable/{tableName}')
async def getTable(tableName):
    return getTableContent(tableName)

@app.post('/setdeviceon')
async def setDeviceOn():
    return deviceON()

@app.post('/setdeviceoff')
async def setDeviceOff():
    return deviceOFF()

@app.post('/senddevicecmd')
async def sendDeviceCMD():
    return sendCMD()

@app.get('/getdevicestatus')
async def getDeviceStatus():
    return sendRQST()


register_tortoise(
    app,
    db_url=creds["sqlite_db_url"],
    modules={'models' : ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)

if __name__ == "__main__":
    uvicorn.run(creds["uvicorn_cfg_title"],
                host = creds["uvicorn_cfg_host"],
                port = int(creds["uvicorn_cfg_port"]))