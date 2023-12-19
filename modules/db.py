from curses.ascii import HT
from fileinput import filename
import os
import boto3
from typing import Any
from boto3.dynamodb.conditions import Key, Attr
from click import password_option
from fastapi import HTTPException
#from models import UserIn_Pydantic, RegisterItem, LoginItem

from passlib.hash import bcrypt as bcrpt
import bcrypt

from datetime import datetime, timedelta

from utils import credentials as creds
from errorHandling import DynamodbErr
from helpers import createDBRecord

constfileName = os.path.basename(__file__)

dynDBErr = DynamodbErr(caller=constfileName)

dynamodb = boto3.resource(  
    service_name=creds["aws_db_service_id"],
    region_name=creds["aws_db_service_region"],
    aws_access_key_id=creds["aws_acc_key_id"],
    aws_secret_access_key=creds["aws_acc_key"]
    )

@dynDBErr.commonDynamodbErrorHandler_dec
def insertRecord(data:dict, tableName:str)-> str or dict:
    table = dynamodb.Table(tableName) # type: ignore
    item = data
    table.put_item(Item= item)
    return "Record inserted successfully!"

@dynDBErr.commonDynamodbErrorHandler_dec
def getTableContent(tableName:str)-> str or dict:
    table = dynamodb.Table(tableName) #type: ignore
    items = table.scan()
    return items["Items"]

@dynDBErr.commonDynamodbErrorHandler_dec
async def reg_user(user: dict)-> str or dict:
    try:
        print(user)
        table = dynamodb.Table("users")
        hashed_password = bcrypt.hashpw(user["password"].encode('utf-8'), bcrypt.gensalt())
        table.put_item(
            Item={
                "username": user["username"],
                "password": hashed_password.decode("utf-8"),
                "email": user["email"]
            }
        )
        return "Successful registration!"
    except HTTPException:
        return str(HTTPException(status_code=400, detail="Invalid information"))

dynDBErr.commonDynamodbErrorHandler_dec
async def login_user(user: dict)-> str or dict:
    try:
        table = dynamodb.Table("users")
        response = table.query(KeyConditionExpression=Key("username").eq(user["username"]))
        if "Items" not in str(response):
            return "User not found"
        hash = str(response["Items"][0]["password"]).encode("utf-8")
        if bcrypt.checkpw(str(user["password"]).encode('utf-8'), hash):
            return f'Logged in, Welcome aboard {user["username"]}! {200}'
        else:
            return f'Invalid Login Info! {400}'
    except AttributeError:
        return f'Provide an Email and Password in JSON format in the request body {400}'


def authenticate_user(user: dict):
    table = dynamodb.Table("users")
    response = table.query(KeyConditionExpression=Key("username").eq(user["username"]))
    if "Items" not in str(response):
        return False
    else:
        return True

# user = {
#     "username": "Zolko1995",
#     "password": "Nissan350"
# }

# print(authenticate_user(user))