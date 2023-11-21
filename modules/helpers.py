import os
import time
import uuid

def checkUserValidity(username:str, func)-> bool:
    return True if func(username) else False

def createDBRecord(key:str, value:str)-> dict:       
    return {
        "pKey": str(uuid.uuid4()),
        "key" : key,
        "value" : value
        }

