import os
from pyclbr import Class
import time
from typing import Any
import boto3.exceptions as dyndbEXC

class debugHelper():
    def __init__(self) -> None:
        pass
    def checkRUNTIME(self ,func):
        def inner(*args: Any, **kwargs: Any):
            t1 = time.time()
            func(*args, **kwargs)
            t2 = time.time() - t1
            print(f"Function {func.__name__} took {t2} seconds to run!")
            return inner


class FileIOErr(debugHelper):
    def __init__(self, fileName: str, caller: str):
        super().__init__()
        self.caller = caller
        self.fileName = fileName
        self.fileExistErr = FileExistsError
        self.fileNotFoundErr = FileNotFoundError
        self.prefix = "[FILE_IO_ERROR]"
        self.fileExistErrMSG = f"{self.prefix}, The file with the name {self.fileName} already exists! {self.caller}"
        self.fileNotFoundErrMSG = f"{self.prefix}, The file with the name {self.fileName} is not found! {self.caller}"

    def commonFileIOErrorHandler_dec(self, func):
        def inner(*args: Any, **kwargs: Any):
            try:
                func(*args, **kwargs)
            except self.fileExistErr:
                return self.fileExistErrMSG
            except self.fileNotFoundErr:
                return self.fileExistErrMSG
            return inner
    
    def showErrorVault(self):
        return [self.fileExistErr, self.fileNotFoundErr]


class DynamodbErr(debugHelper):
    def __init__(self, caller: str):
        super().__init__()
        self.caller = caller
        self.operationNotSupportedErr = dyndbEXC.DynamoDBOperationNotSupportedError
        self.resourceNotExistsErr = dyndbEXC.ResourceNotExistsError
        self.needsConditionErr = dyndbEXC.DynamoDBNeedsConditionError
        self.needsKeyConditionErr = dyndbEXC.DynamoDBNeedsKeyConditionError
        self.prefix = "[DYNAMO_DB_ERROR]"
        self.operationNotSupportedErrMSG = f"{self.prefix} Not supported operation! {self.caller}"
        self.resourceNotExistsErrMSG = f"{self.prefix} Resource does not exist {self.caller}"
        self.needsConditionErrMSG = f"{self.prefix} Condition needed {self.caller}"
        self.needsKeyConditionErrMSG = f"{self.prefix} Key Condition needed {self.caller}"
    
    def commonDynamodbErrorHandler_dec(self, func):
        def inner(*args: Any, **kwargs: Any):
            try:
                func(*args, **kwargs)
            except self.operationNotSupportedErr:
                self.operationNotSupportedErrMSG
            except self.resourceNotExistsErr:
                return self.resourceNotExistsErrMSG
            except self.needsConditionErr:
                return self.needsConditionErrMSG
            except self.needsKeyConditionErr:
                return self.needsKeyConditionErrMSG
            return inner
    
    def showErrorVault(self):
        return [self.operationNotSupportedErr,
                self.resourceNotExistsErr,
                self.needsConditionErr,
                self.needsKeyConditionErr]
        
class FastapiErr(debugHelper):
    def __init__(self):
        super().__init__()