from fileinput import filename
import os
import boto3
from typing import Any
from boto3.dynamodb.conditions import Key, Attr

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
def getRecordByKey(key:str, tableName:str)-> str or dict:
    table = dynamodb.Table(tableName)# type: ignore
    response = table.query(
        KeyConditionExpression=Key(key).eq(key))
    return response["Items"]






#print(createDBRecord("Krumpi", "Hranolky Feri Bacsid"))
#print(createDBRecord("Pástétomos Lekváros Kenyér", "Roxorral"))

#insertRecord(data=dict(frokost), tableName="books")

#print(getTableContent(tableName="books"))
#print(dynDBErr.resourceLoadErrMSG)
