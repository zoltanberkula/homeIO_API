import os
import random
import time
import json
from dotenv import load_dotenv

load_dotenv()

credentials: dict = {
    "aws_acc_key_id" : os.environ.get("AWS_ACCESS_KEY_ID"),
    "aws_acc_key" : os.environ.get("AWS_ACCESS_KEY"),
    "aws_db_service_id" : os.environ.get("AWS_DB_SERVICE_ID"),
    "aws_db_service_region" : os.environ.get("AWS_DB_SERVICE_REGION"),
    "aws_db_table_name" : os.environ.get("AWS_DB_TABLE_NAME"),
    "fast_api_origin_addr" : os.environ.get("FASTAPI_ORIGIN_ADDRESS"),
    "fast_api_token_url" : os.environ.get("FASTAPI_TOKEN_URL"),
    "fast_api_token_type" : os.environ.get("FASTAPI_TOKEN_TYPE"),
    "fast_api_jwt_secret" : os.environ.get("FASTAPI_JWT_SECRET"),
    "sqlite_db_url" : os.environ.get("SQLITE_DB_URL"),
    "uvicorn_cfg_title" : os.environ.get("UVICORN_CFG_TITLE"),
    "uvicorn_cfg_host" : os.environ.get("UVICORN_CFG_HOST_ADDRESS"),
    "uvicorn_cfg_port"  : int(os.environ.get("UVICORN_CFG_PORT")) # type: ignore
}

mqtt_credentials: dict = {
    "mqtt_broker" : os.environ.get("mqtt-broker"),
    "mqtt_port" : os.environ.get("mqtt-port"),
    "mqtt_topic" : os.environ.get("mqtt-topic"),
    "mqtt_username" : os.environ.get("mqtt-username"),
    "mqtt_password" : os.environ.get("mqtt-password"),
    "client_id" : f'python-mqtt-{random.randint(0, 1000)}'
}

aws_credentials: dict = {
    "caCert" : os.environ.get("caCertPath"),
    "certFile" : os.environ.get("certFilePath"),
    "keyFile" : os.environ.get("keyFilePath"),
    "defaultTopic" : os.environ.get("defaultTopic"),
    "devCommandTopic" : os.environ.get("devCommandTopic"),
    "devRequestTopic" : os.environ.get("devRequestTopic"),
    "endpointAWS" : os.environ.get("endpointAWS"),
    "awsPORT" : int(os.environ.get("awsPORT")) # type: ignore
}

def checkRUNTIME(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        func(*args, **kwargs)
        t2 = time.time() - t1
        print(f'{func.__name__} ran in {t2} seconds')
    return wrapper

cmdON: str = "ON"
cmdOFF: str = "OFF"

statusRQST: dict = {
    "devStatus" : "",
    "devState" : ""
}

def generateDevIdentity(devID:str, devType:str, devLoc:str, devState:bool)-> str:
    return json.dumps({
        "devID" : devID,
        "devType" : devType,
        "devLocation" : devLoc,
        "devState" : devState
    })

def generateCommandMSG(devID:str, cmd:str)-> str:
    return json.dumps({
        "devID" : devID,
        "msgType" : "CMD",
        "cmd" : cmd #ON/OFF
    })

def generateRequestMSG(devID:str, rqst:str)-> str:
    return json.dumps({
        "devID" : devID,
        "msgType" : "RQST",
        "rqst" : rqst #STATUS REQ
    })