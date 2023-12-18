from fileinput import filename
import os
import boto3
from typing import Any
from boto3.dynamodb.conditions import Key, Attr
from click import password_option
from fastapi import HTTPException
from models import UserIn_Pydantic

from passlib.hash import bcrypt

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
async def checkUserExistence(username: str, password: str)-> str or dict:
    table = dynamodb.Table("users")# type: ignore
    #response = table.query(KeyConditionExpression=Key(key).eq(key))
    response = await table.get_item(TableName="users", Key={
        "username": username,
        "password_hash": password
    })
    return response

@dynDBErr.commonDynamodbErrorHandler_dec
def checkPasswordValidity(username: str, password: str):
    table = dynamodb.Table("users")
    items = table.scan()
    stored_password = ""
    #print(items)
    for i in range(len(items['Items'])):
        #print(items["Items"][i]["password_hash"])
        if items["Items"][i]["username"] == username:
            stored_password = items["Items"][i]["password_hash"]
    response = table.get_item(Key={
        "username": username,
        "password_hash": password
        })
    #stored_password = response.get('Item, {}').get("password_hash")
    result = bcrypt.verify(password, stored_password)
    print(result)
    # if not stored_password or stored_password != password:
    #     return False
    # else:
    #     return True

@dynDBErr.commonDynamodbErrorHandler_dec
async def registerUser(user: UserIn_Pydantic)-> str or dict: #type: ignore
    table = dynamodb.Table("users")
    #response = table.query(KeyConditionExpression=Key("username").eq(user.username))
    response = checkUserExistence(username=user.username, password=user.password_hash)
    print(response)
    if response != user.username:
        item = {"username": user.username, "password_hash": user.password_hash}
        table.put_item(Item=item)
    else:
        raise HTTPException(status_code=400, detail="User already exists!")
    return {"message" : "User registered successfully"} # type: ignore

@dynDBErr.commonDynamodbErrorHandler_dec
async def loginUser(user: UserIn_Pydantic): #type: ignore
    table = dynamodb.Table("users")
    response = table.get_item(Key={"username": user.username})
    print(response)
    stored_password = response.get('Item',{}).get("password_hash")
    print(stored_password)
    # if not stored_password or stored_password != user.password_hash:
    #     raise
    # HTTPException(status_code=401, detail="Invalid credentials!")
    return {"message": "Login successful!"}
