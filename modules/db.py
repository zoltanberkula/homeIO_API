from typing import Any
import boto3
from boto3.dynamodb.conditions import Key, Attr
from idna import valid_contextj
from utils import credentials as creds
import uuid

import boto3.exceptions as dyndbEXC

from errorHandling import DynamodbErr

dynDBErr = DynamodbErr(caller="dbClient")



caller = "dbClient"
operationNotSupportedErr = dyndbEXC.DynamoDBOperationNotSupportedError
resourceNotExistsErr = dyndbEXC.ResourceNotExistsError
resourceLoadErr = dyndbEXC.ResourceLoadException
needsConditionErr = dyndbEXC.DynamoDBNeedsConditionError
needsKeyConditionErr = dyndbEXC.DynamoDBNeedsKeyConditionError
prefix = "[DYNAMO_DB_ERROR]"
operationNotSupportedErrMSG = f"{prefix} Not supported operation! {caller}"
resourceNotExistsErrMSG = f"{prefix} Resource does not exist {caller}"
needsConditionErrMSG = f"{prefix} Condition needed {caller}"
needsKeyConditionErrMSG = f"{prefix} Key Condition needed {caller}"
resourceLoadErrMSG = f"{prefix} Resource could not be loaded {caller}"

def commonDynamodbErrorHandler_dec(func: Any)-> Any:
    def inner(*args: Any, **kwargs: Any)-> Any:
        try:
            val = func(*args, **kwargs)
        except operationNotSupportedErr:
            return operationNotSupportedErrMSG
        except resourceNotExistsErr:
            return resourceNotExistsErrMSG
        except resourceLoadErr:
            return resourceLoadErrMSG
        except needsConditionErr:
            return needsConditionErrMSG
        except needsKeyConditionErr:
            return needsKeyConditionErrMSG
        return val
    return inner    




dynamodb = boto3.resource(  
    service_name=creds["aws_db_service_id"],
    region_name=creds["aws_db_service_region"],
    aws_access_key_id=creds["aws_acc_key_id"],
    aws_secret_access_key=creds["aws_acc_key"]
    )

@dynDBErr.commonDynamodbErrorHandler_dec
def insertRecord(data:dict, tableName:str)-> str:
    table = dynamodb.Table(tableName) # type: ignore
    item = data
    table.put_item(Item= item)
    return "Record inserted successfully!"

@dynDBErr.commonDynamodbErrorHandler_dec
def getTableContent(tableName:str)-> Any:
    table = dynamodb.Table(tableName) #type: ignore
    items = table.scan()
    return items["Items"]

# @dynDBErr.commonDynamodbErrorHandler_dec
def getRecordByKey(key:str, tableName:str)-> str:
    table = dynamodb.Table(tableName)# type: ignore
    response = table.query(
        KeyConditionExpression=Key(key).eq(key))
    return response["Items"]

frokost = {
    "bookID": str(uuid.uuid4()),
    "name" : "Párky",
    "author" : "Milan Horcica"
}

#insertRecord(data=dict(frokost), tableName="books")

print(getTableContent(tableName="books"))