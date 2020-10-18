import random,time, json, datetime
import numpy as np
'''
This random generator simulate a smoke detector that push a notify only if the patient is smoking.
It is a simple binary value
'''
class ReadingSmoker(object):

    def __init__(self):
        self.msg = {"bn": "",
                   "e":{"subject": "",
                        "value": "",
                        "u": "",
                        "time": ""}}
    def generate(self):
        binary = np.random.choice([0, 1], p=[.5, .5])
        if binary == 0:
            smoke_status = "Smoking"
        else:
            smoke_status = "No Smoking"
        current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        time.sleep(10)
        with open("../Blood_pressure/config_file.json", "r") as f:
            file = f.read()
        f.close()
        config_file = json.loads(file)
        self.msg["bn"] = str(config_file["device_id"])
        self.msg["e"]["subject"] = "Smoker"
        self.msg["e"]["value"] = smoke_status
        self.msg["e"]["u"] = "yes/no variable"
        self.msg["e"]["time"] = str(current_time)

        return json.dumps(self.msg)
