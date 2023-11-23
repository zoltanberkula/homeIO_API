import time
from paho.mqtt import client as mqtt_client
from dataclasses import dataclass
from typing import Optional

from utils import mqtt_credentials as mqttCreds

msg: str

@dataclass
class MQTT_SETTER:
    def connect_mqtt(self)-> mqtt_client.Client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        
        client = mqtt_client.Client(mqttCreds["mqtt-clientid"])
        client.on_connect = on_connect
        client.connect(mqttCreds["mqtt-broker"], mqttCreds["mqtt-port"])
        return client
    
    def publish(self, client: mqtt_client.Client, qos: Optional[int], payload: dict or str)-> None:
        qos = qos or 1
        while True:
            time.sleep(1)
            result = client.publish(mqttCreds["mqtt-topic"], msg)
            status = result[0]
            if status == 0:
                print(f"Send '{msg}' to topic '{mqttCreds["mqtt-topic"]}")
            else:
                print(f"Failed to send message to topic {mqttCreds["mqtt-topic"]}")
            qos = qos + 1
            if qos > 3:
                break
    
    def run(self)-> None:
        client = self.connect_mqtt()
        client.loop_start()
        self.publish(client) # type: ignore
        client.loop_stop()