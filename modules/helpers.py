import os
import time

def checkUserValidity(username:str, func):
    return True if func(username) else False