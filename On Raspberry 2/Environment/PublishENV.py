import paho.mqtt.client as PahoMQTT
import time
import datetime
import requests
import json
import os
from temp_hum import ReadingEnvironmentCondition
import dweepy

class PublishENV(object):

    def __init__(self, url, device_data, sensor, patient_data, broker_ip, broker_port):

        self._paho_mqtt = PahoMQTT.Client(device_data["device_id"], False)
        self._paho_mqtt.on_connect = self.myOnConnect
        self.messageBroker = broker_ip
        self.port = int(broker_port)
        self.url = url
        self.sensor = sensor
        self.patient = patient_data["patient"]
        self.patient_id = patient_data["patient_id"]
        self.name = patient_data["name"]
        self.surname = patient_data["surname"]
        self.age = patient_data["age"]
        self.u = device_data["u"]

    def start(self):
        self._paho_mqtt.connect(self.messageBroker, self.port)
        self._paho_mqtt.loop_start()

    def stop(self):
        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()

    def load_topic(self):
        try:
            respond = requests.get(self.url)
            json_format = json.loads(respond.text)
            self.env_topic = json_format['topic']['Environment_Condition']
        except:
            print("PublishData: ERROR IN CONNECTING TO THE SERVER FOR READING BROKER TOPICS")

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        '''Current time'''
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("Connection acknowledge received with code: %s\nat time %s".format(rc, current_time))


    def myPublish(self):
        try:
            json_format = self.sensor.generate()
            data = json.loads(json_format)
            json_data = json.dumps({'id': patient_id,
                                    'patient': self.patient,
                                   'Name': self.name,
                                   'Surname': self.surname,
                                   'Age': self.age,
                                   'bn': data["bn"],
                                   'e': data['e']
                                   }
                                    )
            msg_info = self._paho_mqtt.publish(self.env_topic, str(json_data), qos=1)
            msg_info.wait_for_publish()
            if msg_info.is_published() == True:
                print("\n\nMessage is published.")
            print('id :'+patient_id+'\npatient :'+self.patient+'\nName :'+self.name+'\nSurname :'+self.surname+'\nAge :'+self.age+'\nbn :'+data["bn"]+'\ne :'+str(data['e']))
            dweepy.dweet_for('progiotdash2_env', data['e'])

        except:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Error in publishing data related to the sensors\nat time %".format(current_time))

if __name__ == '__main__':
    try:
        with open("config_file.json", 'r') as file:
            json_string = file.read()
        file.close()
    except:
        raise KeyError('Error: Reading Config File')

    config_file = json.loads(json_string)
    catalog_ip = config_file["sourceCatalog"]
    patient = config_file["patient"]

    name = config_file["Name"]
    surname = config_file["Surname"]
    age = config_file["Age"]
    device_id = config_file["device_id"]
    u = config_file["u"]

    # Sending the request of the patient ID
    requent = requests.get(os.path.join("http://", catalog_ip, patient))
    json_format = json.loads(requent.text)
    patient_id = json_format["id"]

    patient_data = {"patient_id": patient_id,
                    "patient": patient,
                    "name": name,
                    "surname": surname,
                    "age": age}

    device_data = {"device_id": device_id,
                   "u": u}

    url = os.path.join("http://", catalog_ip, patient)

    sensor = ReadingEnvironmentCondition()
    broker_ip = ""
    broker_port = 0

    try:
        request = requests.get(os.path.join("http://", catalog_ip, "broker"))
        json_format = json.loads(request.text)
        broker_ip = json_format["Broker_IP"]
        broker_port = json_format["Broker_port"]
    except:
        print("ERROR DURING THE READING OF THE BROKER DATA")

    Publisher = PublishENV(url, device_data, sensor, patient_data, broker_ip, broker_port)

    while True:
        Publisher.load_topic()
        Publisher.start()
        while True:
            Publisher.load_topic()
            Publisher.myPublish()
            time.sleep(5)
