from mqttSetter import MQTT_SETTER

mqttSetter = MQTT_SETTER()
mqttSetter.connect_mqtt()
mqttSetter.run()