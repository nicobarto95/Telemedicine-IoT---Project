import numpy as np
import random
import datetime
import json
import time

class ReadingHR(object):

    def __init__(self):
        self.msg = {"bn": "",
                   "e":{"subject": "",
                        "value": "",
                        "u": "",
                        "time": ""}}
    def generate(self):
        hr_random = np.random.choice(np.arange(50,110,5),p=[0.05, 0.09, 0.09, 0.1, 0.1, 0.1, 0.1, 0.09, 0.09, 0.09, 0.05, 0.05])
        current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        time.sleep(50)
        with open("config_file.json", "r") as f:
            file = f.read()
        f.close()
        config_file = json.loads(file)
        self.msg["bn"] = str(config_file["device_id"])
        self.msg["e"]["subject"] = "Heart_Rate"
        self.msg["e"]["value"] = str(hr_random)
        self.msg["e"]["u"] = str(config_file["u"])
        self.msg["e"]["time"] = str(current_time)

        return json.dumps(self.msg)






