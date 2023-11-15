import os
from dotenv import load_dotenv

load_dotenv()

credentials = {
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
