
import datetime
import paho.mqtt.client as PahoMQTT
import requests
import json
import os

''' The Subscriber_WebService is a script that represents the "third class" that has to subscribe data 
from all publishers and it writes the received data into a json file that contains the real time data of the all patients'''

class SubscribeData(object):

    def __init__(self, clientID, topic, broker_ip, broker_port):
        self.client = clientID
        self._paho_mqtt = PahoMQTT.Client(clientID, False)

        self._paho_mqtt.on_connect = self.on_connect
        self._paho_mqtt.on_message = self.on_message

        self.topic = topic
        self.messageBroker = broker_ip
        self.port = int(broker_port)

    def start(self):
        # manage connection to broker
        self._paho_mqtt.connect(self.messageBroker, self.port)

        # subscribe for a topic
        self._paho_mqtt.subscribe(self.topic, qos=1)
        self._paho_mqtt.loop_forever()

    def on_connect(self,paho_mqtt ,userdata, mid, granted_qos):
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print("Subscribed: {} {}".format(mid, granted_qos))
        print("at time: {}".format(current_time))

    def on_message(self,paho_mqtt ,userdata, msg):
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print("Message received at time: {}".format(str(current_time)))
        message_body = str(msg.payload.decode('utf-8'))

        with open('Patients.json','r+') as file:
            json_string = file.read()
        file.close()
        message_input = json.loads(message_body)
        json_format_output = json.loads(json_string)
        subject = message_input['e']["subject"]
        patient = message_input['patient']
        if patient in json_format_output:
            if subject == 'Heart_Rate':
                json_format_output[patient]["Heart_Rate"]["device_id"] = message_input['bn']
                json_format_output[patient]["Heart_Rate"]["value"] = message_input['e']["value"]
                json_format_output[patient]["Heart_Rate"]["u"] = message_input['e']["u"]
                json_format_output[patient]["Heart_Rate"]["time"] = message_input['e']["time"]

            elif (subject == 'Breathing_Rate'):
                json_format_output[patient]["Breathing_Rate"]["device_id"] = message_input["bn"]
                json_format_output[patient]["Breathing_Rate"]["value"] = message_input['e']["value"]
                json_format_output[patient]["Breathing_Rate"]["u"] = message_input['e']["u"]
                json_format_output[patient]["Breathing_Rate"]["time"] = message_input['e']["time"]

            elif subject == 'Blood_Pressure':
                json_format_output[patient]["Blood_Pressure"]["device_id"] = message_input["bn"]
                json_format_output[patient]["Blood_Pressure"]["value"].update(message_input['e']["value"])
                json_format_output[patient]["Blood_Pressure"]["u"] = message_input['e']["u"]
                json_format_output[patient]["Blood_Pressure"]["time"] = message_input['e']["time"]

            elif (subject == "Glucose_Concentration"):
                json_format_output[patient]["Glucose_Concentration"]["device_id"] = message_input["bn"]
                json_format_output[patient]["Glucose_Concentration"]["value"] = message_input['e']["value"]
                json_format_output[patient]["Glucose_Concentration"]["u"] = message_input['e']["u"]
                json_format_output[patient]["Glucose_Concentration"]["time"] = message_input['e']["time"]

            elif (subject == "Saturation_O2"):
                json_format_output[patient]["Saturation_O2"]["device_id"] = message_input["bn"]
                json_format_output[patient]["Saturation_O2"]["value"] = message_input['e']["value"]
                json_format_output[patient]["Saturation_O2"]["u"] = message_input['e']["u"]
                json_format_output[patient]["Saturation_O2"]["time"] = message_input['e']["time"]

            elif (subject == "Environment_Condition"):
                json_format_output[patient]["Environment_Condition"]["value"] = message_input['e']["value"]
                json_format_output[patient]["Environment_Condition"]["device_id"] = message_input["bn"]
                json_format_output[patient]["Environment_Condition"]["time"] = message_input['e']["time"]

            elif (subject == "Body_Temperature"):
                json_format_output[patient]["Body_Temperature"]["device_id"] = message_input["bn"]
                json_format_output[patient]["Body_Temperature"]["value"] = message_input['e']["value"]
                json_format_output[patient]["Body_Temperature"]["u"] = message_input['e']["u"]
                json_format_output[patient]["Body_Temperature"]["time"] = message_input['e']["time"]

            elif (subject == "Smoker"):
                json_format_output[patient]["Smoker"]["device_id"] = message_input["bn"]
                json_format_output[patient]["Smoker"]["value"] = message_input['e']["value"]
                json_format_output[patient]["Smoker"]["u"] = message_input['e']["u"]
                json_format_output[patient]["Smoker"]["time"] = message_input['e']["time"]

        with open("Patients.json", 'w') as real_time_data:
            json.dump(json_format_output, real_time_data)
            real_time_data.close()


if __name__ == "__main__":
    try:
        file = open("config_file.json", "r")
        json_string = file.read()
        file.close()
    except:
        raise KeyError("")

    config_json = json.loads(json_string)
    catalog_url  = config_json["sourceCatalog"]["url"]
    wildcard = config_json["sourceCatalog"]["wildcards"]

    broker_ip = ""
    broker_port = 0

    try:
        request = requests.get(os.path.join(catalog_url,"broker"))
        broker_data = json.loads(request.text)
        broker_ip = broker_data["Broker_IP"]
        broker_port = broker_data["Broker_port"]
    except:
        print("ERROR REQUEST: THE BROKER DATA")
    clientID = "Subscriber"
    Subscriber = SubscribeData(clientID, str(wildcard), broker_ip, broker_port)

    while True:
        Subscriber.start()


