import random, time, datetime
import numpy as np
import json
'''
The reference values for temp are:
-30-32 (high danger)
-33-34 (medium danger)
-35-35.9 (low danger)
-36-36.9 (no danger)
-37-38 (low danger)
-39-40 (medium danger)
-40+ (high danger)
'''


class ReadingBodyTempertature(object):

    def __init__(self):
        self.msg = {"bn": "",
                   "e":{"subject": "",
                        "value": "",
                        "u": "",
                        "time": ""}}
    def generate(self):
        body_temperature = int(np.random.choice(np.arange(36, 37.1, 0.1), p=[0.05, 0.07, 0.09, 0.1, 0.12, 0.13, 0.12, 0.11, 0.09, 0.06, 0.03, 0.03]) * 100) / 100
        current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        time.sleep(60)
        with open("config_file.json", "r") as f:
            file = f.read()
        f.close()
        config_file = json.loads(file)
        self.msg["bn"] = str(config_file["device_id"])
        self.msg["e"]["subject"] = "Body_Temperature"
        self.msg["e"]["value"] = str(body_temperature)
        self.msg["e"]["u"] = str(config_file["u"])
        self.msg["e"]["time"] = str(current_time)

        return json.dumps(self.msg)
