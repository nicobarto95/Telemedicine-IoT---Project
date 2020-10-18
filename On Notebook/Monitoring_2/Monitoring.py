import requests
import json
import os
import paho.mqtt.client as PahoMQTT
import time
import dweepy

''' The Monitoring is a python code that makes some requests to the catalog for the topics, the thresholds, criticals for the health of the patient, and the current sensors values and it also 
    is a publisher of information about those value, if they are positive, in normal range, or if they are not, so probably there is an emerrgency '''

class TrackingSystem(object):
    def __init__(self, url, patient, patient_id, broker_ip, broker_port):
        self.catalog_url = url
        self.patient = patient
        self.patient_id = patient_id
        self._paho_mqtt = PahoMQTT.Client(patient_id, False)
        self._paho_mqtt.on_connect = self.on_connect
        self._paho_mqtt.on_message = self.on_message

        self.messageBroker = broker_ip
        self.port = int(broker_port)

        '''Initialization of the threshold values and the value too'''
        '''Heart Rate'''
        self.hr = 0
        self.hr_u = 0
        self.hr_max = 0
        self.hr_min = 0
        '''Blood pressure'''
        self.bp_min = 0
        self.bp_max = 0
        self.bp_u = 0
        # Normal Diastolic range
        self.bp_ndia_max = 0
        self.bp_ndia_min = 0
        # Normal Sistolic range
        self.bp_nsi_max = 0
        self.bp_nsi_min = 0
        # High Diastolic range
        self.bp_hdia_max = 0
        self.bp_hdia_min = 0
        # High Sistolic range
        self.bp_hsi_max = 0
        self.bp_hsi_min = 0
        # Very High Diastolic range
        self.bp_vhdia_max = 0
        self.bp_vhdia_min = 0
        # Very High Sistolic range
        self.bp_vhsi_max = 0
        self.bp_vhsi_min = 0
        # Dangerous Diastolic range
        self.bp_ddia_max = 0
        self.bp_ddia_min = 0
        # Dangerous Sistolic range
        self.bp_dsi_max = 0
        self.bp_dsi_min = 0
        '''Hypoxemia'''
        self.so2 = 0
        self.so2_u = 0
        # Slight Hypoxemia range
        self.so2_slight_max = 0
        self.so2_slight_min = 0
        # Moderate Hypoxemia range
        self.so2_moderate_max = 0
        self.so2_moderate_min = 0
        # Serious Hypoxemia range
        self.so2_serious_max = 0
        self.so2_serious_min = 0
        '''Breathing Rate'''
        self.br = 0
        self.br_u = 0
        self.br_max = 0
        self.br_min = 0
        '''Temperature'''
        self.temperature = 0
        self.temperature_u = 0
        self.temp_freez_min = 0
        self.temp_freez_max = 0
        self.temp_vcold_min = 0
        self.temp_vcold_max = 0
        self.temp_cold_min = 0
        self.temp_cold_max = 0
        self.temp_comfort_min = 0
        self.temp_comfort_max = 0
        self.temp_warm_min = 0
        self.temp_warm_max = 0
        self.temp_vwarm_min = 0
        self.temp_vwarm_max = 0
        self.temp_boil_min = 0
        self.temp_boil_max = 0
        '''Glucose level'''
        self.glu = 0
        self.glu_u = 0
        self.glu_vlow_min = 0
        self.glu_low_min = 0
        self.glu_norm_min = 0
        self.glu_high_min = 0
        self.glu_vhigh_min = 0
        self.glu_vlow_max = 0
        self.glu_low_max = 0
        self.glu_norm_max = 0
        self.glu_high_max = 0
        self.glu_vhigh_max = 0
        '''Environmental comfort ranges'''
        self.env = 0
        self.env_tempC_u = 0
        self.env_tempF_u = 0
        self.env_hum_u = 0
        self.env_tempC_min = 0
        self.env_tempC_max = 0
        self.env_tempF_min = 0
        self.env_tempF_max = 0
        self.env_hum_min = 0
        self.env_hum_max = 0
        '''Smoker value'''
        self.smoke = ""

    def start(self):
        # manage connection to broker
        self._paho_mqtt.connect(self.messageBroker, self.port)
        self._paho_mqtt.loop_start()
        # subscribe for a topic


    def stop(self):
        # manage connection to broker
        self._paho_mqtt.loop_stop()
        # unsubscribed command
        self._paho_mqtt.disconnect()

    def on_connect(self, paho_mqtt, userdata, flags, rc):
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print("Connection to {} with the result {}".format(self.messageBroker, rc))
        print("at time: {}".format(current_time))

    def on_message(self, paho_mqtt, userdata, msg):
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print("Topic: {}".format(msg.topic))
        print("QoS: {}".format(str(msg.qos)))
        print("Message received {}".format(str(msg.payload)))
        print("at time: {}".format(str(current_time)))

    def loading(self):
        # At first, try to sending requests to the MQTT to the WebService to obtain
        # the current values of the patient
        try:
            request = requests.get(os.path.join(self.catalog_url, "Data_for_Rest"))
            json_request = json.loads(request.text)
            self.rest_url = json_request["Host_IP"]
            self.rest_port = json_request["port"]

            request = requests.get(os.path.join(self.catalog_url, self.patient))
            json_request = json.loads(request.text)
        except:
            print("REQUEST ERROR: THE DATA FROM WEB SERVICE")

        # Heart Rate
        self.hr_topic = json_request["topic"]["Heart_Rate"]
        self.hr_u = json_request["thresholds"]["hr"]["u"]
        self.hr_min = json_request["thresholds"]["hr"]["min"]
        self.hr_max = json_request["thresholds"]["hr"]["max"]
        dweepy.dweet_for("pro1_thr_hr", {"max": self.hr_max, "min": self.hr_min, "u": self.hr_u})

        # Blood Pressure
        self.bp_topic = json_request["topic"]["Blood_Pressure"]
        self.bp_u = json_request["thresholds"]["bp"]["u"]
        # Normal Diastolic range
        self.bp_ndia_max = json_request["thresholds"]["bp"]["normal"]["diastolic"]["max"]
        self.bp_ndia_min = json_request["thresholds"]["bp"]["normal"]["diastolic"]["min"]
        dweepy.dweet_for("pro1_thr_bp_d", {"max": self.bp_ndia_max, "min": self.bp_ndia_min, "u": self.bp_u})

        # Normal Sistolic range
        self.bp_nsi_max = json_request["thresholds"]["bp"]["normal"]["systolic"]["max"]
        self.bp_nsi_min = json_request["thresholds"]["bp"]["normal"]["systolic"]["min"]
        dweepy.dweet_for("pro1_thr_bp_s", {"max": self.bp_nsi_max, "min": self.bp_nsi_min, "u": self.bp_u})

        # High Diastolic range
        self.bp_hdia_max = json_request["thresholds"]["bp"]["high"]["diastolic"]["max"]
        self.bp_hdia_min = json_request["thresholds"]["bp"]["high"]["diastolic"]["min"]
        # High Sistolic range
        self.bp_hsi_max = json_request["thresholds"]["bp"]["high"]["systolic"]["max"]
        self.bp_hsi_min = json_request["thresholds"]["bp"]["high"]["systolic"]["min"]
        # Very High Diastolic range
        self.bp_vhdia_max = json_request["thresholds"]["bp"]["very_high"]["diastolic"]["max"]
        self.bp_vhdia_min = json_request["thresholds"]["bp"]["very_high"]["diastolic"]["min"]
        # Very High Sistolic range
        self.bp_vhsi_max = json_request["thresholds"]["bp"]["very_high"]["systolic"]["max"]
        self.bp_vhsi_min = json_request["thresholds"]["bp"]["very_high"]["systolic"]["min"]
        # Dangerous Diastolic range
        self.bp_ddia_max = json_request["thresholds"]["bp"]["dangerous"]["diastolic"]["max"]
        self.bp_ddia_min = json_request["thresholds"]["bp"]["dangerous"]["diastolic"]["min"]
        # Dangerous Sistolic range
        self.bp_dsi_max = json_request["thresholds"]["bp"]["dangerous"]["systolic"]["max"]
        self.bp_dsi_min = json_request["thresholds"]["bp"]["dangerous"]["systolic"]["min"]

        # Saturation O2
        self.so2_topic = json_request["topic"]["Saturation_O2"]
        self.so2_u = json_request["thresholds"]["hypoxemia"]["u"]
        self.so2_slight_max = json_request["thresholds"]["hypoxemia"]["slight"]["max"]
        self.so2_slight_min = json_request["thresholds"]["hypoxemia"]["slight"]["min"]
        self.so2_moderate_max = json_request["thresholds"]["hypoxemia"]["moderate"]["max"]
        self.so2_moderate_min = json_request["thresholds"]["hypoxemia"]["moderate"]["min"]
        self.so2_serious_max = json_request["thresholds"]["hypoxemia"]["serious"]["max"]
        self.so2_serious_min = json_request["thresholds"]["hypoxemia"]["serious"]["min"]
        dweepy.dweet_for("pro1_thr_so2", {"slight_limit": self.so2_slight_max, "moderate_limit": self.so2_moderate_max, "serious_limit": self.so2_serious_max, "u": self.so2_u})

        # Breating Rate
        self.br_topic = json_request["topic"]["Breathing_Rate"]
        self.br_u = json_request["thresholds"]["breathing_rate"]["u"]
        self.br_max = json_request["thresholds"]["breathing_rate"]["max"]
        self.br_min = json_request["thresholds"]["breathing_rate"]["min"]
        dweepy.dweet_for("pro1_thr_br", {"max": self.br_max, "min": self.br_min, "u": self.br_u})

        # Temperature
        self.temperature_topic = json_request["topic"]["Body_Temperature"]
        self.temperature_u = json_request["thresholds"]["temperature"]["u"]
        self.temp_freez_min = json_request["thresholds"]["temperature"]["freezing"]["min"]
        self.temp_freez_max = json_request["thresholds"]["temperature"]["freezing"]["max"]
        self.temp_vcold_min = json_request["thresholds"]["temperature"]["very_cold"]["min"]
        self.temp_vcold_max = json_request["thresholds"]["temperature"]["very_cold"]["max"]
        self.temp_cold_min = json_request["thresholds"]["temperature"]["cold"]["min"]
        self.temp_cold_max = json_request["thresholds"]["temperature"]["cold"]["max"]
        self.temp_comfort_min = json_request["thresholds"]["temperature"]["comfort"]["min"]
        self.temp_comfort_max = json_request["thresholds"]["temperature"]["comfort"]["max"]
        self.temp_warm_min = json_request["thresholds"]["temperature"]["warm"]["min"]
        self.temp_warm_max = json_request["thresholds"]["temperature"]["warm"]["max"]
        self.temp_vwarm_min = json_request["thresholds"]["temperature"]["very_warm"]["min"]
        self.temp_vwarm_max = json_request["thresholds"]["temperature"]["very_warm"]["max"]
        self.temp_boil_min = json_request["thresholds"]["temperature"]["boil"]["min"]
        self.temp_boil_max = json_request["thresholds"]["temperature"]["boil"]["max"]
        dweepy.dweet_for("pro1_thr_temp", {"freeze": self.temp_freez_max, "very cold": self.temp_vcold_max, "cold": self.temp_cold_max, "normal max": self.temp_comfort_max,  "normal min": self.temp_comfort_min,  "warm": self.temp_warm_min, "very warm": self.temp_vwarm_min, "boil": self.temp_boil_min})

        # Glucose level
        self.glu_topic = json_request["topic"]["Glucose_Concentration"]
        self.glu_u = json_request["thresholds"]["glucose_levels"]["u"]
        self.glu_vlow_min = json_request["thresholds"]["glucose_levels"]["very_low"]["min"]
        self.glu_low_min = json_request["thresholds"]["glucose_levels"]["low"]["min"]
        self.glu_norm_min = json_request["thresholds"]["glucose_levels"]["normal"]["min"]
        self.glu_high_min = json_request["thresholds"]["glucose_levels"]["high"]["min"]
        self.glu_vhigh_min = json_request["thresholds"]["glucose_levels"]["very_high"]["min"]
        self.glu_vlow_max = json_request["thresholds"]["glucose_levels"]["very_low"]["max"]
        self.glu_low_max = json_request["thresholds"]["glucose_levels"]["low"]["max"]
        self.glu_norm_max = json_request["thresholds"]["glucose_levels"]["normal"]["max"]
        self.glu_high_max = json_request["thresholds"]["glucose_levels"]["high"]["max"]
        self.glu_vhigh_max = json_request["thresholds"]["glucose_levels"]["very_high"]["max"]
        dweepy.dweet_for("pro1_thr_glu", {"very low": self.glu_vlow_max, "low": self.glu_low_max, "normal max": self.glu_norm_max,  "normal min": self.glu_norm_min,  "high": self.glu_high_min, "very high": self.glu_vhigh_min})

        # Environmental igrometric comfort ranges
        self.env_topic = json_request["topic"]["Environment_Condition"]
        self.env_tempC_u = json_request["thresholds"]["comfort_range"]["t_C"]["u"]
        self.env_tempF_u = json_request["thresholds"]["comfort_range"]["t_F"]["u"]
        self.env_hum_u = json_request["thresholds"]["comfort_range"]["hum"]["u"]
        self.env_tempC_min = json_request["thresholds"]["comfort_range"]["t_C"]["min"]
        self.env_tempC_max = json_request["thresholds"]["comfort_range"]["t_C"]["max"]
        self.env_tempF_min = json_request["thresholds"]["comfort_range"]["t_F"]["min"]
        self.env_tempF_max = json_request["thresholds"]["comfort_range"]["t_F"]["max"]
        self.env_hum_min = json_request["thresholds"]["comfort_range"]["hum"]["min"]
        self.env_hum_max = json_request["thresholds"]["comfort_range"]["hum"]["max"]

        # Smoker topic
        self.smoke_topic = json_request["topic"]["Smoker"]

    def checking_temperature(self):
        global msg, obj
        self.bodytemp_notifier = ""

        msg = ""
        subject = "Body Temperature"
        if (self.temp_freez_min <= self.temperature["value"] <= self.temp_freez_max) or (
                self.temp_boil_min <= self.temperature["value"] <= self.temp_boil_max):
            msg = "EMERGENCY - The temperature is ABNOMAL!!!! "
            obj = "Red code"
        elif (self.temp_vcold_min <= self.temperature["value"] <= self.temp_vcold_min) or (
                self.temp_vwarm_min <= self.temperature["value"] <= self.temp_vwarm_max):
            msg = "Emergency - The temperature is out of range, CALL the patient!!!! "
            obj = "Yellow code"
        elif (self.temp_cold_min <= self.temperature["value"] <= self.temp_cold_max) or (
                self.temp_warm_min <= self.temperature["value"] <= self.temp_warm_max):
            msg = "The patient is into an alterad state, the temperature is lightly out of range "
            obj = "Yellow code"
        '''elif (self.temp_comfort_min <= self.temperature["value"] <= self.temp_comfort_max):
            msg = "The patient temperature is into the comfort range "
            obj = "None"'''
        if msg:
            self.bodytemp_notifier = json.dumps({"subject": subject,
                                                 "patient": self.patient,
                                                 "patient_id": self.patient_id,
                                                 "status": msg,
                                                 "object": obj,
                                                 "value": self.temperature["value"],
                                                 "u": self.temperature_u,
                                                 "time": str(self.temperature["time"])
                                                 })
            dweepy.dweet_for("pro1_out_bt", {"value": 1})
        else:
            dweepy.dweet_for("pro1_out_bt", {"value": 0})


    def checking_bp(self):
        global msg, obj
        self.bp_notifier = ""

        msg = ""
        subject = "Blood Pressure"
        if (self.bp["value"]["Diastolic"] < self.bp_ddia_max > self.bp_ddia_min) or (
                self.bp["value"]["Systolic"] < self.bp_dsi_max > self.bp_dsi_min):
            msg = "EMERGENCY - The blood pressure is ABNOMAL!!!! "
            obj = "Red code"
        elif (self.bp_vhdia_min < self.bp_vhdia_max > self.bp["value"]["Diastolic"]) or (
                self.bp["value"]["Systolic"] < self.bp_vhsi_max > self.bp_vhsi_min):
            msg = "Emergency - The blood pressure is out of range, CALL the patient!!!! "
            obj = "Yellow code"

        elif (self.bp["value"]["Diastolic"] < self.bp_hdia_max > self.bp_hdia_min) or (
                self.bp["value"]["Systolic"] < self.bp_hsi_max > self.bp_hsi_min):
            msg = "The blood pressure is out of range, CALL the patient!!!! "
            obj = "White code"

        '''elif (self.bp["value"]["Diastolic"] < self.bp_ndia_max > self.bp_ndia_min) or (
                self.bp["value"]["Systolic"] < self.bp_nsi_max > self.bp_nsi_min):
            msg = "The patient temperature is into the comfort range "
            obj = "None"'''
        if msg:

            self.bp_notifier = json.dumps({"subject": subject,
                                       "patient": self.patient,
                                       "patient_id": self.patient_id,
                                       "status": msg,
                                       "object": obj,
                                       "value": {"Systolic": self.bp["value"]["Systolic"],
                                                 "Diastolic": self.bp["value"]["Diastolic"]},
                                       "u": self.bp_u,
                                       "time": self.bp["time"]
                                       })
            dweepy.dweet_for("pro1_out_bp", {"value": 1})
        else:
            dweepy.dweet_for("pro1_out_bp", {"value": 0})

    def checking_hr(self):
        global msg, obj
        self.hr_notifier = ""

        msg = ""
        subject = "Heart Rate"
        if not (self.hr_min < self.hr["value"] < self.hr_max):
            msg = "Heart Rate out of range"
            obj = "Yellow code"
        if msg:
            self.hr_notifier = json.dumps({"subject": subject,
                                       "patient": self.patient,
                                       "patient_id": self.patient_id,
                                       "status": msg,
                                       "object": obj,
                                       "value": self.hr["value"],
                                       "u": self.bp_u,
                                       "time": self.hr["time"]
                                       })
            dweepy.dweet_for("pro1_out_hr", {"value": 1})
        else:
            dweepy.dweet_for("pro1_out_hr", {"value": 0})

    def checking_glu(self):
        global msg, obj
        self.glu_notifier = ""

        msg = ""
        subject = "Glucose_concentration"
        if (self.glu_vlow_min < self.glu["value"] < self.glu_vlow_max) or (
                self.glu_vhigh_min < self.glu["value"] < self.glu_vhigh_max):
            msg = "EMERGENCY - The glucose concentration is ABNOMAL!!!! "
            obj = "Red code"
        elif (self.glu_low_min < self.glu["value"] < self.glu_low_max) or (
                self.glu_high_min < self.glu["value"] < self.glu_high_max):
            msg = "The blood pressure is out of range, CALL the patient!!!! "
            obj = "White code"
        '''elif (self.glu_norm_min < self.glu["value"] < self.glu_norm_max):
            msg = "The glucose concentration of the patient is into the normal range "
            obj = "None"'''
        if msg:
            self.glu_notifier = json.dumps({"subject": subject,
                                        "patient": self.patient,
                                        "patient_id": self.patient_id,
                                        "status": msg,
                                        "object": obj,
                                        "value": self.glu["value"],
                                        "u": self.bp_u,
                                        "time": self.glu["time"]
                                        })
            dweepy.dweet_for("pro1_out_glu", {"value": 1})
        else:
            dweepy.dweet_for("pro1_out_glu", {"value": 0})

    def checking_environment(self):
        global msg, obj
        self.env_notifier = ""

        msg = ""
        subject = "Temperature C"
        if not (self.env_tempC_min <= self.env["value"]["Temperature (C)"] <= self.env_tempC_max) or not (self.env_tempF_min <= self.env["value"]["Temperature (F)"] <= self.env_tempF_max):
            msg = "The environment temperature is out of range"
            obj = "Modify the temperature"


        tempC_notifier = {"subject": subject,
                          "status": msg,
                          "object": obj,
                          "value": self.env["value"]["Temperature (C)"],
                          "u": "C",
                          "time": self.env["time"]
                          }
        subject = "Temperature F"
        tempF_notifier = {
            "subject": subject,
            "status": msg,
            "object": obj,
            "value": self.env["value"]["Temperature (F)"],
            "u": "F",
            "time": self.env["time"]
        }

        subject = "Humidity (%)"
        hum_notifier = {
            "subject": subject,
            "status": msg,
            "object": obj,
            "value": self.env["value"]["Humidity (%)"],
            "u": "%",
            "time": self.env["time"]
        }
        if msg:

            self.env_notifier = json.dumps({"subject": "Environment Condition",
                                        "patient": self.patient,
                                        "patient_id": self.patient_id,
                                        "Temperature C": tempC_notifier,
                                        "Temperature F": tempF_notifier,
                                        "Humidity %": hum_notifier,
                                        "time": self.env["time"]})


    def checking_br(self):
        global msg, obj
        self.br_notifier = ""
        msg = ""
        subject = "Breathing Rate"
        if not (self.br_min < self.br["value"] < self.br_max):
            msg = "The breathing is out of range"
            object = "Yellow code"
        '''else:
            msg = "The breathing is into the optimal range"
            object = "None"'''
        if msg:
            self.br_notifier = json.dumps({"subject": subject,
                                       "patient": self.patient,
                                       "patient_id": self.patient_id,
                                       "status": msg,
                                       "object": object,
                                       "value": self.br["value"],
                                       "u": self.br["u"],
                                       "time": self.br["time"]})
            dweepy.dweet_for("pro1_out_br", {"value": 1})
        else:
            dweepy.dweet_for("pro1_out_br", {"value": 0})

    def checking_so2(self):
        global msg, obj
        self.so2_notifier = ""

        msg = ""
        subject = "Saturation O2"
        if (self.so2_slight_min < self.so2["value"] < self.so2_slight_max):
            msg = "The hypoxemia is slight"
            obj = "White code"
        elif (self.so2_moderate_min < self.so2["value"] < self.so2_moderate_max):
            msg = "Emergency: The hypoxemia is moderate"
            obj = "Yellow code"
        elif (self.so2_serious_min < self.so2["value"] < self.so2_serious_max):
            msg = "EMERGENCY: The hypoxemia is serious!!"
            obj = "Red code"
        '''else:
            msg = "The saturation of O2 is perfect"
            obj = "None"'''
        if msg:
            self.so2_notifier = json.dumps(
            {"subject": subject, "patient": patient, "patient_id": self.patient_id, "status": msg, "object": obj,
             "value": self.so2["value"], "u": self.so2["u"], "time": str(self.so2["time"])})
            dweepy.dweet_for("pro1_out_so2", {"value": 1})
        else:
            dweepy.dweet_for("pro1_out_so2", {"value": 0})

    def checking_smoke(self):
        global msg, obj
        self.smoke_notifier = ""

        msg = ""
        subject = "Smoker"
        if (self.smoke["value"] == "Smoking"):
            msg = "The patient is smoking"
            obj = "Yellow code"

        if msg:
            self.smoke_notifier = json.dumps({"subject": subject, "patient": patient, "patient_id": self.patient_id, "status": msg, "object": obj, "value": self.smoke["value"], "u": self.smoke["u"], "time": str(self.smoke["time"])})
            dweepy.dweet_for("pro1_out_smo", {"value": 1})
        else:
            dweepy.dweet_for("pro1_out_smo", {"value": 0})

    def monitoring_threshold(self):

        self.hr = json.loads(requests.get("http://" + self.rest_url + ":" + str(self.rest_port) + "/" + self.patient + "/hr").text.replace("\'", "\""))
        self.br = json.loads(requests.get("http://" + self.rest_url + ":" + str(self.rest_port) + "/" + self.patient + "/br").text.replace("\'", "\""))
        self.bp = json.loads(requests.get("http://" + self.rest_url + ":" + str(self.rest_port) + "/" + self.patient + "/bp_status").text.replace("\'", "\""))
        self.so2 = json.loads(requests.get("http://" + self.rest_url + ":" + str(self.rest_port) + "/" + self.patient + "/sO2").text.replace("\'", "\""))
        self.temperature = json.loads(requests.get("http://" + self.rest_url + ":" + str(self.rest_port) + "/" + self.patient + "/t").text.replace("\'", "\""))
        self.glu = json.loads(requests.get("http://" + self.rest_url + ":" + str(self.rest_port) + "/" + self.patient + "/gc").text.replace("\'", "\""))
        self.env = json.loads(requests.get("http://" + self.rest_url + ":" + str(self.rest_port) + "/" + self.patient + "/env_condition").text.replace("\'", "\""))
        self.smoke = json.loads(requests.get("http://" + self.rest_url + ":" + str(self.rest_port) + "/" + self.patient + "/smoker").text.replace("\'", "\""))

        # Checking threshold

        self.checking_temperature()
        self.checking_bp()
        self.checking_hr()
        self.checking_glu()
        self.checking_environment()
        self.checking_br()
        self.checking_so2()
        self.checking_smoke()

        try:
            if (self.bodytemp_notifier):
                temperature_publish = self._paho_mqtt.publish(self.temperature_topic, str(self.bodytemp_notifier), qos=0)
                temperature_publish.wait_for_publish()
                if temperature_publish.is_published() == True:
                    print("\n\nBody Temperature status is published.")
                print("patient_id :"+str(json.loads(self.bodytemp_notifier)["patient_id"]))
                print("subject :"+str(json.loads(self.bodytemp_notifier)["subject"]))
                print("value:"+str(json.loads(self.bodytemp_notifier)["value"]))
                print("status :"+ str(json.loads(self.bodytemp_notifier)["status"]))
                print("object :" + str(json.loads(self.bodytemp_notifier)["object"]))

            if (self.bp_notifier):
                blood_pressure_publish = self._paho_mqtt.publish(self.bp_topic, str(self.bp_notifier), qos=0)
                blood_pressure_publish.wait_for_publish()
                if blood_pressure_publish.is_published() == True:
                    print("\n\nBlood Pressure status is published.")
                print("patient_id :" + str(json.loads(self.bp_notifier)["patient_id"]))
                print("subject :" + str(json.loads(self.bp_notifier)["subject"]))
                print("value:" + str(json.loads(self.bp_notifier)["value"]))
                print("status :" + str(json.loads(self.bp_notifier)["status"]))
                print("object :" + str(json.loads(self.bp_notifier)["object"]))

            if (self.hr_notifier):
                heart_rate_publish = self._paho_mqtt.publish(self.hr_topic, str(self.hr_notifier), qos=0)
                heart_rate_publish.wait_for_publish()
                if heart_rate_publish.is_published() == True:
                    print("\n\nHeart Rate is published.")
                print("patient_id :" + str(json.loads(self.hr_notifier)["patient_id"]))
                print("subject :" + str(json.loads(self.hr_notifier)["subject"]))
                print("value:" + str(json.loads(self.hr_notifier)["value"]))
                print("status :" + str(json.loads(self.hr_notifier)["status"]))
                print("object :" + str(json.loads(self.hr_notifier)["object"]))

            if (self.glu_notifier):
                glucose_level_publish = self._paho_mqtt.publish(self.glu_topic, str(self.glu_notifier), qos=0)
                glucose_level_publish.wait_for_publish()
                if glucose_level_publish.is_published() == True:
                    print("\n\nGlucose Level is published.")
                print("patient_id :" + str(json.loads(self.glu_notifier)["patient_id"]))
                print("subject :" + str(json.loads(self.glu_notifier)["subject"]))
                print("value:" + str(json.loads(self.glu_notifier)["value"]))
                print("status :" + str(json.loads(self.glu_notifier)["status"]))
                print("object :" + str(json.loads(self.glu_notifier)["object"]))

            if (self.env_notifier):
                environment_condition_publish = self._paho_mqtt.publish(self.env_topic, str(self.env_notifier), qos=0)
                environment_condition_publish.wait_for_publish()
                if environment_condition_publish.is_published() == True:
                    print("\n\nEnvironment Condition is published.")
                print("patient_id :" + str(json.loads(self.env_notifier)["patient_id"]))
                print("subject :" + str(json.loads(self.env_notifier)["subject"]))
                print("Temperature C" + str(json.loads(self.env_notifier)["Temperature C"]))
                print("status Temperature " + str(json.loads(self.env_notifier)["Temperature C"]["status"]))
                print("Temperature F" + str(json.loads(self.env_notifier)["Temperature F"]))
                print("Humidity %" + str(json.loads(self.env_notifier)["Humidity %"]))
                print("status Humidity %" + str(json.loads(self.env_notifier)["Humidity %"]["status"]))
                print("object :" + str(json.loads(self.env_notifier)["Temperature C"]["object"]))

            if (self.br_notifier):
                breathing_rate_publish = self._paho_mqtt.publish(self.br_topic, str(self.br_notifier), qos=0)
                breathing_rate_publish.wait_for_publish()
                if breathing_rate_publish.is_published() == True:
                    print("\n\nBreathing Rate is published.")
                print("patient_id :" + str(json.loads(self.br_notifier)["patient_id"]))
                print("subject :" + str(json.loads(self.br_notifier)["subject"]))
                print("value:" + str(json.loads(self.br_notifier)["value"]))
                print("status :" + str(json.loads(self.br_notifier)["status"]))
                print("object :" + str(json.loads(self.br_notifier)["object"]))

            if (self.so2_notifier):
                saturationO2_publish = self._paho_mqtt.publish(self.so2_topic, str(self.so2_notifier), qos=0)
                saturationO2_publish.wait_for_publish()
                if saturationO2_publish.is_published() == True:
                    print("\n\nSaturation O2 is published.")
                print("patient_id :" + str(json.loads(self.so2_notifier)["patient_id"]))
                print("subject :" + str(json.loads(self.so2_notifier)["subject"]))
                print("value:" + str(json.loads(self.so2_notifier)["value"]))
                print("status :" + str(json.loads(self.so2_notifier)["status"]))
                print("object :" + str(json.loads(self.so2_notifier)["object"]))

            if (self.smoke_notifier):
                smoker_publish = self._paho_mqtt.publish(self.smoke_topic, str(self.smoke_notifier), qos=0)
                smoker_publish.wait_for_publish()
                if smoker_publish.is_published() == True:
                    print("\n\nSmoking Status is published.")
                print("patient_id :" + str(json.loads(self.smoke_notifier)["patient_id"]))
                print("subject :" + str(json.loads(self.smoke_notifier)["subject"]))
                print("value:" + str(json.loads(self.smoke_notifier)["value"]))
                print("status :" + str(json.loads(self.smoke_notifier)["status"]))
                print("object :" + str(json.loads(self.smoke_notifier)["object"]))
        except:
            print("ERROR IN PUBLISHING SENSOR DATA")


if __name__ == '__main__':

    try:
        with open("config_file.json", "r") as f:
            config_file = f.read()
        f.close()
    except:
        print("ERROR DURING READING CONFIG FILE")

    config_file = json.loads(config_file)

    catalog_url = config_file["sourceCatalog"]["url"]
    patient = config_file["sourceCatalog"]["patient"]

    try:
        request = requests.get(os.path.join(catalog_url, patient))
        patient_data = json.loads(request.text)
        patient_ip = patient_data["id"]
    except:
        print("ERROR REQUEST: READING PATIENT DATA")

    try:
        request = requests.get(os.path.join(catalog_url, "broker"))
        broker_data = json.loads(request.text)
        broker_ip = broker_data["Broker_IP"]
        broker_port = broker_data["Broker_port"]
    except:
        print("ERROR REQUEST: READING THE BROKER DATA")

    Check = TrackingSystem(catalog_url, patient, patient_ip, broker_ip, broker_port)

    while True:
        Check.start()
        Check.loading()
        Check.monitoring_threshold()
        Check.stop()
        time.sleep(10)
