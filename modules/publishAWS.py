import time
import messageType as msgForm
from connectAWS import publish_data

from utils import aws_credentials, generateCommandMSG, generateRequestMSG
from utils import cmdON, cmdOFF, statusRQST

tpc = aws_credentials["defaultTopic"]

def onOFF(wait: int = 3)-> None:
    while(True):
        publish_data(tpc, msgForm.commandsON["RELAY_1_ON"])
        time.sleep(wait)
        publish_data(tpc, msgForm.commandsOFF["RELAY_1_OFF"])
        time.sleep(wait)

def deviceON(wait: int = 3)-> None:
    publish_data(tpc, msgForm.commandsON["RELAY_1_ON"])
    time.sleep(wait)

def deviceOFF(wait: int = 3)-> None:
    publish_data(tpc, msgForm.commandsOFF["RELAY_1_OFF"])
    time.sleep(wait)

def sendCMD(wait: int = 3)-> None:
    while(True):
        publish_data(tpc, generateCommandMSG("1", cmdON))
        time.sleep(wait)
        publish_data(tpc, generateCommandMSG("1", cmdOFF))
        time.sleep(wait)

def sendRQST(wait: int = 3)-> None:
        publish_data(tpc, generateRequestMSG("1", statusRQST)) # type: ignore
        time.sleep(wait)
        publish_data(tpc, generateRequestMSG("1", statusRQST)) # type: ignore
        time.sleep(wait)