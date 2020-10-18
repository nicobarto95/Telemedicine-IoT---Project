import numpy as np
import datetime
import json
import time
class ReadingBreathingRate(object):

    def __init__(self):
        self.msg = {"bn": "",
                   "e":{"subject": "",
                        "value": "",
                        "u": "",
                        "time": ""}}
    def generate(self):
        br_random = np.random.choice(np.arange(10,20,1),p=[0.05, 0.05, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1, 0.05, 0.05])
        current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        time.sleep(100)
        with open("config_file.json", "r") as f:
            file = f.read()
        f.close()
        config_file = json.loads(file)
        self.msg["bn"] = str(config_file["device_id"])
        self.msg["e"]["subject"] = "Breathing_Rate"
        self.msg["e"]["value"] = str(br_random)
        self.msg["e"]["u"] = config_file["u"]
        self.msg["e"]["time"] = str(current_time)

        return json.dumps(self.msg)
