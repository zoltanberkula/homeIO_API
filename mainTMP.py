from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise import fields
from passlib.hash import bcrypt
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic.creator import pydantic_model_creator
from tortoise.models import Model
import jwt
import boto3
import boto3.exceptions as botoexception
from boto3.dynamodb.conditions import Key, Attr
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uuid
from typing import List
import os
import uvicorn

from modules.utils import credentials as creds

app = FastAPI()

dynamodb = boto3.resource(service_name=creds["aws_db_service_id"],
                          region_name=creds["aws_db_service_region"],
                          aws_access_key_id=creds["aws_acc_key_id"],
                          aws_secret_access_key=creds["aws_acc_key"])

origins = [
    creds["fast_api_origin_addr"],
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)

    @classmethod
    async def get_user(cls, username: str):
        return cls.get(username=username)
    
    def verify_password(self, password: str):
        return bcrypt.verify(password, self.password_hash)
    
User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user

@app.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid username or password'
                            )
    
    user_obj = await User_Pydantic.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), creds["fast_api_jwt_secret"]) # type: ignore
    return {
            'access_token' : token,
            'token_type' : creds["fast_api_token_type"]
            }


@app.post('/users', response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic): # type: ignore
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

async def get_current_user(token: str = Depends(oauth2_scheme)): # type: ignore
    try:
        payload = jwt.decode(token, creds["fast_api_jwt_secret"], algorithms=["HS256"]) # type: ignore
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    return await User_Pydantic.from_tortoise_orm(user)


@app.get('/users/me', response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_user)): # type: ignore
    return user

@app.get('/')
def read_root():
    return "Hello Homepage!"

@app.post('/submitdata')
async def submitdata(data:dict):
    try:
        table = dynamodb.Table(creds["aws_db_table_name"]) # type: ignore

        item= {
            'bookID' : str(uuid.uuid4()),
            'name' : data['name'],
            'author': data['author']
        }
        table.put_item(Item= item)
        return "Data submitted successfully"
    except botoexception.DynamoDBOperationNotSupportedError:
        return "Error NOT SUPPORTED OPERATION!"
    except botoexception.ResourceNotExistsError:
        return "Error RESOURCE DOES NOT EXIST!"


@app.get('/getAllBooks')
def getall():
    try:
        table = dynamodb.Table(creds["aws_db_table_name"]) #type: ignore
        items = table.scan()
        return items
    except botoexception.DynamoDBOperationNotSupportedError:
        return "Error NOT SUPPORTED OPERATION!"
    except botoexception.ResourceNotExistsError:
        return "Error RESOURCE DOES NOT EXIST!"

@app.get('/getUser')
async def getUser(username:str):
    try:
        table = dynamodb.Table(creds["aws_db_table_name"]) #type: ignore
        response = table.query(
            KeyConditionExpression=Key("username").eq(username))
        return response["Items"]
    except botoexception.DynamoDBOperationNotSupportedError:
        return "Error Operation Not supported!"

@app.get('/checkUser')
def checkUserExistence(username:str):
    try:
        table = dynamodb.Table(creds["aws_db_table_name"]) #type: ignore
        response = table.query(
            KeyConditionExpression=Key("bookID").eq(username))
        print(response["Items"][0]["bookID"])
        print(response["Items"][0]["author"])
        print(response["Items"][0]["name"])
        return True if (response["Items"]) else False
    except botoexception.DynamoDBOperationNotSupportedError:
        return "Error Operation Not supported!"
    

def checkUserValidity(username:str):
    if checkUserExistence(username):
        return True
    else:
        return False



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