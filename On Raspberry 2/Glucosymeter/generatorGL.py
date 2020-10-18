import random
import time
import json
import datetime
import numpy as np

'''
-dangerously low : <50 (risk high)
-low : 50-71 (risk low)
-normal : 72-108 (no risk) 
-a little high : 109-120 (low risk)
-high : 121-180 (medium risk)
-very high : 181-280 (high risk)
-dangerously high: >280 (very high risk)

All the units for pressure are in mg/dL
'''
class ReadingGLU(object):

    def __init__(self):
        self.msg = {"bn": "",
                   "e":{"subject": "",
                        "value": "",
                        "u": "",
                        "time": ""}}
    def generate(self):
        glu = np.random.choice(np.arange(80, 116, 3),p=[0.05, 0.07, 0.09, 0.1, 0.12, 0.13, 0.12, 0.11, 0.09, 0.06, 0.03, 0.03])
        current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        time.sleep(30)
        with open("config_file.json", "r") as f:
            file = f.read()
        f.close()
        config_file = json.loads(file)
        self.msg["bn"] = str(config_file["device_id"])
        self.msg["e"]["subject"] = "Glucose_Concentration"
        self.msg["e"]["value"] = str(glu)
        self.msg["e"]["u"] = str(config_file["u"])
        self.msg["e"]["time"] = str(current_time)

        return json.dumps(self.msg)

'''
        To keep in mind for the visualization of glucose levels:
        the reading for glucose leves in hospitalized patients happens
        every 30 min of in less severe cases more rarely. Normally it
        should be 4-5 times a day.
'''
    