
'''The optimal humidity [%] in hospital rooms is 40-60%, we can create the incresing danger alerts every +-10%(?)
The optimal temperature is between >20°(winter) and <24°(summer), we can create the incresing danger alerts every +-2°(?)
'''


import numpy as np
import datetime
import json
import time

class ReadingEnvironmentCondition(object):

    def __init__(self):
        self.msg = {"bn": "",
                   "e":{"subject": "",
                        "value": "",
                        "u": "",
                        "time": ""}}
    def generate(self):
        temp = np.random.choice(np.arange(20, 25, 0.5),p=[0.05, 0.05, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1, 0.05, 0.05])
        hum = np.random.choice(np.arange(40, 60, 2),p=[0.05, 0.05, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1, 0.05, 0.05])
        current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        time.sleep(10)
        with open("config_file.json", "r") as f:
            file = f.read()
        f.close()
        config_file = json.loads(file)
        self.msg["bn"] = str(config_file["device_id"])
        self.msg["e"]["subject"] = "Environment_Condition"
        self.msg["e"]["value"] = {
                                "Temperature (C)": str(temp),
                                "Temperature (F)": str((temp*9/5) + 32),
                                "Humidity (%)": str(hum)}
        self.msg["e"]["time"] = str(current_time)

        return json.dumps(self.msg)


    
