from ast import Call
import os
import time
from typing import Any, Callable
import uuid
import threading
from threading import Timer

class ThreadJob(threading.Thread):
    def __init__(self, callback: Callable, event, interval):
        self.callback = callback,
        self.event = event,
        self.interval = interval
        super(ThreadJob,self).__init__()

    def doJob(self)-> None:
        while not self.event.wait(self.interval): # type: ignore
            self.callback() # type: ignore

def setInterval(func, time):
    e = threading.Event()
    while not e.wait(time):
        func()

def log():
    print("Hallo Verden")

def checkUserValidity(username:str, func)-> bool:
    return True if func(username) else False

def createDBRecord(key:str, value:str)-> dict:       
    return {
        "pKey": str(uuid.uuid4()),
        "key" : key,
        "value" : value
        }

class WithThread(threading.Thread):
    def __init__(self, target: Callable, *args: Any):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)
