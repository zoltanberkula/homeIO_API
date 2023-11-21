import os
from pyclbr import Class
import time
from typing import Any, Callable
import boto3.exceptions as dyndbEXC

class debugHelper():
    def __init__(self):
        pass
    def checkRUNTIME(self ,func: Callable):
        def inner(*args: Any, **kwargs: Any)-> Any:
            t1 = time.time()
            funcVal = func(*args, **kwargs)
            t2 = time.time() - t1
            print(f"Function {func.__name__} took {t2} seconds to run!")
            return funcVal
        return inner

class FileIOErr(debugHelper):
    def __init__(self, fileName: str, caller: str)-> None:
        super().__init__()
        self.caller = caller
        self.fileName = fileName
        self.fileExistErr = FileExistsError
        self.fileNotFoundErr = FileNotFoundError
        self.prefix = "[FILE_IO_ERROR]"
        self.fileExistErrMSG = f"{self.prefix}, The file with the name {self.fileName} already exists! {[self.caller]}"
        self.fileNotFoundErrMSG = f"{self.prefix}, The file with the name {self.fileName} is not found! {[self.caller]}"

    def commonFileIOErrorHandler_dec(self, func: Callable)-> Any:
        def inner(*args: Any, **kwargs: Any)-> Any:
            try:
                funcVal = func(*args, **kwargs)
            except self.fileExistErr:
                return self.fileExistErrMSG
            except self.fileNotFoundErr:
                return self.fileExistErrMSG
            return funcVal
        return inner
    
    def showErrorVault(self):
        return [self.fileExistErr, self.fileNotFoundErr]

class DynamodbErr(debugHelper):
    def __init__(self, caller: str)-> None:
        super().__init__()
        self.caller = caller
        self.operationNotSupportedErr = dyndbEXC.DynamoDBOperationNotSupportedError
        self.resourceNotExistsErr = dyndbEXC.ResourceNotExistsError
        self.resourceLoadErr = dyndbEXC.ResourceLoadException
        self.needsConditionErr = dyndbEXC.DynamoDBNeedsConditionError
        self.needsKeyConditionErr = dyndbEXC.DynamoDBNeedsKeyConditionError
        self.prefix = "[DYNAMO_DB_ERROR]"
        self.operationNotSupportedErrMSG = f"{self.prefix} Not supported operation! {[self.caller]}"
        self.resourceNotExistsErrMSG = f"{self.prefix} Resource does not exist {[self.caller]}"
        self.needsConditionErrMSG = f"{self.prefix} Condition needed {[self.caller]}"
        self.needsKeyConditionErrMSG = f"{self.prefix} Key Condition needed {[self.caller]}"
        self.resourceLoadErrMSG = f"{self.prefix} Resource could not be loaded {[self.caller]}"
    
    def commonDynamodbErrorHandler_dec(self, func: Callable)-> Any:
        def inner(*args: Any, **kwargs: Any):
            try:
                funcVal = func(*args, **kwargs)
            except self.operationNotSupportedErr:
                self.operationNotSupportedErrMSG
            except self.resourceNotExistsErr:
                return self.resourceNotExistsErrMSG
            except self.resourceLoadErr:
                return self.resourceLoadErrMSG
            except self.needsConditionErr:
                return self.needsConditionErrMSG
            except self.needsKeyConditionErr:
                return self.needsKeyConditionErrMSG           
            return funcVal
        return inner
    
    def showErrorVault(self)-> str:
        return str([self.operationNotSupportedErr,
                self.resourceNotExistsErr,
                self.needsConditionErr,
                self.needsKeyConditionErr,
                self.resourceLoadErr])
        
class FastapiErr(debugHelper):
    def __init__(self):
        super().__init__()