import random, time, datetime, json
import numpy as np
'''
The reference values for SpO2 are:
-100% situation of iperventilation (low danger)
-96%-98% normal (no danger)
-93%-95% mild O2 deprivaion (low danger)
-90%-92% low O2 (medium danger)
-<90% (high danger)
'''
class ReadingSP(object):

    def __init__(self):
        self.msg = {"bn": "",
                   "e":{"subject": "",
                        "value": "",
                        "u": "",
                        "time": ""}}
    def generate(self):
        spo2 = np.random.choice(np.arange(93.5, 99.5, 0.5),p=[0.03, 0.03, 0.04, 0.05, 0.06, 0.09, 0.12, 0.14, 0.15, 0.14, 0.1, 0.05 ])
        current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        time.sleep(60)
        with open("config_file.json", "r") as f:
            file = f.read()
        f.close()
        config_file = json.loads(file)
        self.msg["bn"] = str(config_file["device_id"])
        self.msg["e"]["subject"] = "Saturation_O2"
        self.msg["e"]["value"] = str(spo2)
        self.msg["e"]["u"] = str(config_file["u"])
        self.msg["e"]["time"] = str(current_time)

        return json.dumps(self.msg)
