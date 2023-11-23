from ast import Call
import os
import time
from typing import Callable
import uuid
import threading

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

import functools
import sched, time

s = sched.scheduler(time.time, time.sleep)

def setInterval(sec):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*argv, **kwargs):
            setInterval(sec)(func)
            func(*argv, **kwargs)
        s.enter(sec, 1, wrapper, ())
        return wrapper
    s.run()
    return decorator


@setInterval(sec=0.5)
def testInterval():
  print ("test Interval ")

#testInterval()