from typing import Any

commandsON: dict = {
    "RELAY_1_ON": "ON1",
    "RELAY_2_ON": "ON2",
    "RELAY_3_ON": "ON3",
    "RELAY_4_ON": "ON4",
}

commandsOFF: dict = {
    "RELAY_1_OFF": "OFF1",
    "RELAY_2_OFF": "OFF2",
    "RELAY_3_OFF": "OFF3",
    "RELAY_4_OFF": "OFF4",
}

commandMSG: dict = {
    "devID" : str,
    "msgType" : str,
    "cmd" : str
}

requestMSG: dict = {
    "devID" : str,
    "msgType" : str,
    "rqst" : str
}

mqtt_payload: dict = {
    "deviceID" : "",
    "deviceType" : "",
    "deviceLocation" : "",
    "deviceState" : ""
}

mqtt_command: dict = {
    "deviceID" : "",
    "command" : ""
}

mqtt_status: dict = {
    "deviceID" : "",
    "deviceType" : "",
    "deviceLocation" : "",
    "deviceState" : ""
}

def fillScheme(*args)-> Any:
    if args[-1] == "payload" or args[-1] == "status":
        return f"id {args[0]} type {args[1]} location {args[2]} state {args[3]}"
    if args[-1] == "command":
        return f"id {args[0]} command {args[1]}"
    else:
        return 0
    
def createMQTT_PAYLOAD(devID: str, devType: str, devLoc: str, devState: str)-> str:
    mqtt_payload["deviceID"] = devID
    mqtt_payload["deviceType"] = devType
    mqtt_payload["deviceLocation"] = devLoc
    mqtt_payload["devState"] = devState
    return fillScheme(devID, devType, devLoc, devState, str("payload"))

def createMQTT_COMMAND(devID: str, cmd: str)-> str:
    mqtt_command["deviceID"] = devID
    mqtt_command["command"] = cmd
    return fillScheme(devID, cmd, str("command"))

def createMQTT_STATUS_REQUEST(devID: str, devType: str, devLoc: str, devState: str)-> str:
    mqtt_status["deviceID"] = devID
    mqtt_status["deviceType"] = devType
    mqtt_status["deviceLocation"] = devLoc
    mqtt_status["deviceState"] = devState
    return fillScheme(devID, devType, devLoc, devState, str("status"))