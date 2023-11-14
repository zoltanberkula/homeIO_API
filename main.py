from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise import fields
from passlib.hash import bcrypt
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
import jwt
import boto3
import boto3.exceptions as botoexception
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uuid
from typing import List
import os
import time
from dotenv import load_dotenv

load_dotenv()

aws_acc_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_acc_key = os.environ.get("AWS_ACCESS_KEY")
aws_db_service_id = os.environ.get("AWS_DB_SERVICE_ID")
aws_db_service_region = os.environ.get("AWS_DB_SERVICE_REGION")
aws_db_table_name = os.environ.get("AWS_DB_TABLE_NAME")

fast_api_origin_addr = os.environ.get("FASTAPI_ORIGIN_ADDRESS")
fast_api_token_url = os.environ.get("FASTAPI_TOKEN_URL")
fast_api_token_type = os.environ.get("FASTAPI_TOKEN_TYPE")
fast_api_jwt_secret = os.environ.get("FASTAPI_JWT_SECRET")

sqlite_db_url = os.environ.get("SQLITE_DB_URL")


app = FastAPI()

dynamodb = boto3.resource(service_name=aws_db_service_id,
                          region_name=aws_db_service_region,
                          aws_access_key_id=aws_acc_key_id,
                          aws_secret_access_key=aws_acc_key)

origins = [
    fast_api_origin_addr,
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
    async def get_user(cls, username):
        return cls.get(username=username)
    
    def verify_password(self, password):
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
    token = jwt.encode(user_obj.dict(), fast_api_jwt_secret)
    return {
            'access_token' : token,
            'token_type' : fast_api_token_type
            }


@app.post('/users', response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, fast_api_jwt_secret, algorithms=["HS256"])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    return await User_Pydantic.from_tortoise_orm(user)


@app.get('/users/me', response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_user)):
    return user

@app.get('/')
def read_root():
    return "Hello Homepage!"

@app.post('/submitdata')
async def submitdata(data:dict):
    try:
        table = dynamodb.Table(aws_db_table_name)

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
        table = dynamodb.Table(aws_db_table_name)
        items = table.scan()
        return items
    except botoexception.DynamoDBOperationNotSupportedError:
        return "Error NOT SUPPORTED OPERATION!"

register_tortoise(
    app,
    db_url=sqlite_db_url,
    modules={'models' : ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)