from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import jwt
from passlib.hash import bcrypt
from tortoise.contrib.fastapi import register_tortoise

from models import User, User_Pydantic, UserIn_Pydantic, oauth2_scheme, RegisterItem, LoginItem
from db import insertRecord, getTableContent, registerUser, loginUser, reg_user, login_user
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

async def generateToken(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid username or password')
    
    user_obj = await User_Pydantic.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), creds["fast_api_jwt_secret"])
    return {
        "access_token" : token,
        "token_type" : creds["fast_api_token_type"]
    }

async def createUser(user: UserIn_Pydantic): # type: ignore
    # user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    # await user_obj.save()
    # print(user_obj.username)
    # await registerUser(user_obj)
    # return await User_Pydantic.from_tortoise_orm(user_obj)
    return reg_user(user)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, creds["fast_api_jwt_secret"], algorithms=["HS256"])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    return await User_Pydantic.from_tortoise_orm(user)

async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


@app.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await generateToken(form_data) # type: ignore
    
@app.post('/register')
async def create_user(user: dict): #type: ignore
    #print(user)
    return await reg_user(user)

@app.post('/login')
async def login(user: dict): #type: ignore
    #print(user)
    return await login_user(user)

# @app.get('/users/me', response_model=User_Pydantic)
# async def get_user(user: User_Pydantic = Depends(get_current_user)): # type: ignore
#     return user

# @app.get('/')
# async def read_root():
#     return "HELLO THERE!!!"

# @app.post('/submitdata')
# async def submitData(data: dict):
#     return insertRecord(data, creds["aws_db_table_name"])

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