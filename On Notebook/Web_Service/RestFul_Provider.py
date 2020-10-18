import cherrypy
import json
import requests

'''
This script retrives informations with GET methods from the "Data_for_Rest" url for each patient data  
'''

class RestFul_Provider(object):
    exposed = True
    def GET(self, *uri, **params):
        item = uri[0]
        with open("Patients.json", "r") as file:
            json_string = file.read()
        file.close()
        json_content = json.loads(json_string)

        if item in json_content:
            if (uri[1] == "name"):
                return str(json_content[item]["Name"])
            elif (uri[1] == "surname"):
                return str(json_content[item]["Surname"])
            elif (uri[1] == "hr"):
                return str(json_content[item]["Heart_Rate"])
            elif (uri[1] == "bp_status"):
                return str(json_content[item]["Blood_Pressure"])
            elif (uri[1] == "br"):
                return str(json_content[item]["Breathing_Rate"])
            elif (uri[1] == "gc"):
                return str(json_content[item]["Glucose_Concentration"])
            elif (uri[1] == "sO2"):
                return str(json_content[item]["Saturation_O2"])
            elif (uri[1] == "env_condition"):
                return str(json_content[item]["Environment_Condition"])
            elif (uri[1] == "t"):
                return str(json_content[item]["Body_Temperature"])
            elif (uri[1] == "smoker"):
                return str(json_content[item]["Smoker"])
            elif (uri[1] == "all"):
                return str(json.dumps(json_content[item]))  
        else:
            return ("Try again with another input")

if __name__=="__main__":
    with open("config_file.json","r") as file:
        json_string = file.read()
    file.close()

    config_file = json.loads(json_string)
    url = config_file["sourceCatalog"]["url"]
    req = requests.get(url+'Data_for_Rest')
    json_format = json.loads(req.text)

    Host_IP = json_format["Host_IP"]
    Port = json_format["port"]

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True
        }
    }

    cherrypy.tree.mount(RestFul_Provider(), '/', conf)
    cherrypy.config.update({
        "server.socket_host": str(Host_IP),
        "server.socket_port": int(Port)
    })
    cherrypy.engine.start()
    cherrypy.engine.block()
