import paho.mqtt.client as mqtt_client
import ssl
from utils import aws_credentials as awsCreds
from utils import checkRUNTIME

def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IOT" + str(rc))

awsClient = mqtt_client.Client()
awsClient.on_connect = on_connect
awsClient.tls_set(ca_certs=awsCreds["caCert"],
                  certfile=awsCreds["certFile"],
                  keyfile=awsCreds["keyFile"],
                  tls_version=ssl.PROTOCOL_SSLv23)
awsClient.tls_insecure_set(True)

def connectAWS()-> None:
    awsClient.connect(awsCreds["endpointAWS"], awsCreds["awsPORT"], 60)
    awsClient.loop()

@checkRUNTIME
def publish_data(topic: str, payload: str or dict):
    connectAWS()
    print(f"Publishing {payload} to {topic}")
    awsClient.publish(topic, payload, qos=0, retain=False)