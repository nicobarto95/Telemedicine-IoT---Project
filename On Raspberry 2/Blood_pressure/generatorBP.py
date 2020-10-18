import random,time, json, datetime
import numpy as np
'''
The parameters for pressure are sistolic/diastolic/mean
-The normal parameter are sistolic 100-130, diastolic 60-80
-High pressure sistolic 130 - 135, diastolic 80 - 85 (low level danger)
-Very high pressure sistolic 135 - 160, diastolic 88 - 100 (medium level danger)
-Dangerous pressure sistolic 160+, distolic 100+ (high level danger)

All the units for pressure are in mmHg
'''
class ReadingBP(object):

    def __init__(self):
        self.msg = {"bn": "",
                   "e":{"subject": "",
                        "value": "",
                        "u": "",
                        "time": ""}}
    def generate(self):
        systolic = np.random.choice(np.arange(85, 145, 5), p=[0.05, 0.09, 0.09, 0.1, 0.1, 0.1, 0.1, 0.09, 0.09, 0.09, 0.05, 0.05])
        diastolic = np.random.choice(np.arange(40, 100, 5), p=[0.05, 0.09, 0.09, 0.1, 0.1, 0.1, 0.1, 0.09, 0.09, 0.09, 0.05, 0.05])
        current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        time.sleep(10)
        with open("config_file.json", "r") as f:
            file = f.read()
        f.close()
        config_file = json.loads(file)
        self.msg["bn"] = str(config_file["device_id"])
        self.msg["e"]["subject"] = "Blood_Pressure"
        self.msg["e"]["value"] = {"Systolic": str(systolic),
                                  "Diastolic": str(diastolic)}
        self.msg["e"]["u"] = str(config_file["u"])
        self.msg["e"]["time"] = str(current_time)

        return json.dumps(self.msg)
