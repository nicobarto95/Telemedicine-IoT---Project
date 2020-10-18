#!/usr/bin/env python

import time
import datetime
import cherrypy
import json
import numpy as np
import os
from os import path
import pandas as pd
import pathlib as Path
import ast

class SourceCatalog(object):
    exposed = True

    def check_availability(self, element, collection: iter):
        return element in collection

    def GET(self, *uri, **params):
        # The GET works properly!
        # Opening of the JSON file with the patients data
        try:
            with open("data.json", 'r') as f:
                json_dict = json.loads(f.read())
                f.close()
                '''The possible options are:
                                            - patient_1
                                            - patient_2
                                            - broker
                                            - Telegram_Bot
                                            - Data_for_Rest
                                            - Date_time'''
                item = uri[0]
        except:
            raise KeyError("ERROR: THE READING OF THE DATA.JSON")

        if item in json_dict:
            if len(uri) == 1:
                data = json_dict[item]
                requested_data = json.dumps(data)
            elif len(uri) == 2:
                data = json_dict[item][uri[1]]
                requested_data = json.dumps(data)
            elif len(uri) == 3:
                data = json_dict[item][uri[1]][uri[2]]
                requested_data = json.dumps(data)
            elif len(uri) == 4:
                data = json_dict[item][uri[1]][uri[2]][uri[3]]
                requested_data = json.dumps(data)
            return requested_data
        else:
            return "YOUR CHOISE RETURNED NOTHING"

    def POST(self, *uri, **params):
        try:
            with open("data.json", "r") as f:
                initial_data = json.loads(f.read())
            f.close()
            item = uri[0]
            patients = json.loads(cherrypy.request.body.read())
            key = list(patients.keys())[0]

            if key == 'id':
                if item in initial_data:
                    if key in initial_data[item]:
                        initial_data[item]['id'] = patients['id']
                        print("\n")
                        print("Updating...")
                        time.sleep(1)
                        print("The file 'data.json' is updated:\nThe new {} of the {} is {}".format(key, item, initial_data[item]['id']))
                        print('at time: {}'.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
                        print("\n\n")

                    else:
                        temp_json = {'id': patients['id']}
                        initial_data[item].update(temp_json)
                        print("\n")
                        print("Updating...")
                        time.sleep(1)
                        print("The file 'data.json' is updated:\nThe new {} of the {} is {}".format(key, item, temp_json))
                        print('at time: {}'.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
                        print("\n\n")

                else:
                    initial_data[item] = {}
                    temp_json = {'id': patients['id']}
                    initial_data[item].update(temp_json)
                    print("\n")
                    print("Updating...")
                    time.sleep(1)
                    print("The file 'data.json' is updated:\nThe new patient is posted!\nThe new {} of the {} is {}".format(key, item, temp_json))
                    print('at time: {}'.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
                    print("\n\n")

            if key == 'topic':
                if item in initial_data:
                    if key in initial_data[item]:
                        initial_data[item]['topic']['Clinical_situation'] = patients['topic']['Clinical_situation']
                        initial_data[item]['topic']['Name'] = patients['topic']['Name']
                        initial_data[item]['topic']['Surname'] = patients['topic']['Surname']
                        initial_data[item]['topic']['Heart_Rate'] = patients['topic']['Heart_Rate']
                        initial_data[item]['topic']['Blood_Pressure'] = patients['topic']['Blood_Pressure']
                        initial_data[item]['topic']['Breathing_Rate'] = patients['topic']['Breathing_Rate']
                        initial_data[item]['topic']['Glucose_Concentration'] = patients['topic']['Glucose_Concentration']
                        initial_data[item]['topic']['Saturation_O2'] = patients['topic']['Saturation_O2']
                        initial_data[item]['topic']['Body_Temperature'] = patients['topic']['Body_Temperature']
                        initial_data[item]['topic']['Environment_Condition'] = patients['topic']['Environment_Condition']
                        initial_data[item]['topic']['Smoker'] = patients['topic']['Smoker']
                        print("\n")
                        print("Updating...")
                        time.sleep(1)
                        print("The file 'data.json' is updated:\nThe new {} of the {} is {}".format(key, item, initial_data[item]['topic']))
                        print('at time: {}'.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
                        print("\n\n")

                    else:
                        temp_json = {'topic':{"Clinical_situation": patients['topic']['Clinical_situation'],
                                      "Name": patients['topic']['Name'],
                                      "Surname": patients['topic']['Surname'],
                                      "Age": patients['topic']['Age'],
                                      "Heart_Rate": patients['topic']['Heart_Rate'],
                                      "Blood_Pressure": patients['topic']['Blood_Pressure'],
                                      "Breathing_Rate": patients['topic']['Breathing_Rate'],
                                      "Glucose_Concentration": patients['topic']['Glucose_Concentration'],
                                      "Saturation_O2": patients['topic']['Saturation_O2'],
                                      "Body_Temperature": patients['topic']['Body_Temperature'],
                                      "Environment_Condition": patients['topic']['Environment_Condition'],
                                      "Smoker": patients['topic']['Smoker']
                                      }}
                        initial_data[item].update(temp_json)
                        print("\n")
                        print("Updating...")
                        time.sleep(1)
                        print("The file 'data.json' is updated:\nThe new {} of the {} is {}".format(key, item, temp_json))
                        print('at time: {}'.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
                        print("\n\n")

                else:
                    initial_data[item] = {}
                    temp_json = {'topic': {"Clinical_situation": patients['topic']['Clinical_situation'],
                                  "Name": patients['topic']['Name'],
                                  "Surname": patients['topic']['Surname'],
                                  "Age": patients['topic']['Age'],
                                  "Heart_Rate": patients['topic']['Heart_Rate'],
                                  "Blood_Pressure": patients['topic']['Blood_Pressure'],
                                  "Breathing_Rate": patients['topic']['Breathing_Rate'],
                                  "Glucose_Concentration": patients['topic']['Glucose_Concentration'],
                                  "Saturation_O2": patients['topic']['Saturation_O2'],
                                  "Body_Temperature": patients['topic']['Body_Temperature'],
                                  "Environment_Condition": patients['topic']['Environment_Condition'],
                                  "Smoker": patients['topic']['Smoker']
                                  }}
                    initial_data[item].update(temp_json)
                    print("\n")
                    print("Updating...")
                    time.sleep(1)
                    print("The file 'data.json' is updated:\nThe new patient is posted!\nThe new {} of the {} is {}".format(key, item, temp_json))
                    print('at time: {}'.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
                    print("\n\n")

            if key == 'thresholds':
                if item in initial_data:
                    if key in initial_data[item]:
                        initial_data[item]['thresholds']['hr']['u'] = patients['thresholds']['hr']['u']
                        initial_data[item]['thresholds']['hr']['min'] = patients['thresholds']['hr']['min']
                        initial_data[item]['thresholds']['hr']['max'] = patients['thresholds']['hr']['max']

                        initial_data[item]['thresholds']['bp']['u'] = patients['thresholds']['bp']['u']
                        initial_data[item]['thresholds']['bp']['normal']['diastolic'] = patients['thresholds']['bp']['normal']['diastolic']
                        initial_data[item]['thresholds']['bp']['normal']['systolic'] = patients['thresholds']['bp']['normal']['systolic']
                        initial_data[item]['thresholds']['bp']['high']['diastolic'] = patients['thresholds']['bp']['high']['diastolic']
                        initial_data[item]['thresholds']['bp']['high']['systolic'] = patients['thresholds']['bp']['high']['systolic']
                        initial_data[item]['thresholds']['bp']['very_high']['diastolic'] = patients['thresholds']['bp']['very_high']['diastolic']
                        initial_data[item]['thresholds']['bp']['very_high']['systolic'] = patients['thresholds']['bp']['very_high']['systolic']
                        initial_data[item]['thresholds']['bp']['dangerous']['diastolic'] = patients['thresholds']['bp']['dangerous']['diastolic']
                        initial_data[item]['thresholds']['bp']['dangerous']['systolic'] = patients['thresholds']['bp']['dangerous']['systolic']

                        initial_data[item]['thresholds']['hypoxemia']['u'] = patients['thresholds']['hypoxemia']['u']
                        initial_data[item]['thresholds']['hypoxemia']['slight']['min'] = patients['thresholds']['hypoxemia']['slight']['min']
                        initial_data[item]['thresholds']['hypoxemia']['slight']['max'] = patients['thresholds']['hypoxemia']['slight']['max']
                        initial_data[item]['thresholds']['hypoxemia']['moderate']['min'] = patients['thresholds']['hypoxemia']['moderate']['min']
                        initial_data[item]['thresholds']['hypoxemia']['moderate']['max'] = patients['thresholds']['hypoxemia']['moderate']['max']
                        initial_data[item]['thresholds']['hypoxemia']['serious']['min'] = patients['thresholds']['hypoxemia']['serious']['min']
                        initial_data[item]['thresholds']['hypoxemia']['serious']['max'] = patients['thresholds']['hypoxemia']['serious']['max']

                        initial_data[item]['thresholds']['breathing_rate']['u'] = patients['thresholds']['breathing_rate']['u']
                        initial_data[item]['thresholds']['breathing_rate']['min'] = patients['thresholds']['breathing_rate']['min']
                        initial_data[item]['thresholds']['breathing_rate']['max'] = patients['thresholds']['breathing_rate']['max']

                        initial_data[item]['thresholds']['temperature']['u '] = patients['thresholds']['temperature']['u']
                        initial_data[item]['thresholds']['temperature']['freezing']['min'] = patients['thresholds']['temperature']['freezing']['min']
                        initial_data[item]['thresholds']['temperature']['freezing']['max'] = patients['thresholds']['temperature']['freezing']['max']
                        initial_data[item]['thresholds']['temperature']['very_cold']['min'] = patients['thresholds']['temperature']['very_cold']['min']
                        initial_data[item]['thresholds']['temperature']['very_cold']['max'] = patients['thresholds']['temperature']['very_cold']['max']
                        initial_data[item]['thresholds']['temperature']['cold']['min'] = patients['thresholds']['temperature']['cold']['min']
                        initial_data[item]['thresholds']['temperature']['cold']['max'] = patients['thresholds']['temperature']['cold']['max']
                        initial_data[item]['thresholds']['temperature']['comfort']['min'] = patients['thresholds']['temperature']['comfort']['min']
                        initial_data[item]['thresholds']['temperature']['comfort']['max'] = patients['thresholds']['temperature']['comfort']['max']
                        initial_data[item]['thresholds']['temperature']['warm']['min'] = patients['thresholds']['temperature']['warm']['min']
                        initial_data[item]['thresholds']['temperature']['warm']['max'] = patients['thresholds']['temperature']['warm']['max']
                        initial_data[item]['thresholds']['temperature']['very_warm']['min'] = patients['thresholds']['temperature']['very_warm']['min']
                        initial_data[item]['thresholds']['temperature']['very_warm']['max'] = patients['thresholds']['temperature']['very_warm']['max']
                        initial_data[item]['thresholds']['temperature']['boil']['min'] = patients['thresholds']['temperature']['boil']['min']
                        initial_data[item]['thresholds']['temperature']['boil']['max'] = patients['thresholds']['temperature']['boil']['max']

                        initial_data[item]['thresholds']['glucose_levels']['u'] = patients['thresholds']['glucose_levels']['u']
                        initial_data[item]['thresholds']['glucose_levels']['very_low']['min'] = patients['thresholds']['glucose_levels']['very_low']['min']
                        initial_data[item]['thresholds']['glucose_levels']['very_low']['max'] = patients['thresholds']['glucose_levels']['very_low']['max']
                        initial_data[item]['thresholds']['glucose_levels']['low']['min'] = patients['thresholds']['glucose_levels']['low']['min']
                        initial_data[item]['thresholds']['glucose_levels']['low']['max'] = patients['thresholds']['glucose_levels']['low']['max']
                        initial_data[item]['thresholds']['glucose_levels']['normal']['min'] = patients['thresholds']['glucose_levels']['normal']['min']
                        initial_data[item]['thresholds']['glucose_levels']['normal']['max'] = patients['thresholds']['glucose_levels']['normal']['max']
                        initial_data[item]['thresholds']['glucose_levels']['high']['min'] = patients['thresholds']['glucose_levels']['high']['min']
                        initial_data[item]['thresholds']['glucose_levels']['high']['max'] = patients['thresholds']['glucose_levels']['high']['max']
                        initial_data[item]['thresholds']['glucose_levels']['very_high']['min'] = patients['thresholds']['glucose_levels']['very_high']['min']
                        initial_data[item]['thresholds']['glucose_levels']['very_high']['max'] = patients['thresholds']['glucose_levels']['very_high']['max']

                        initial_data[item]['thresholds']['comfort_range']['t_C']['u'] = patients['thresholds']['comfort_range']['t_C']['u']
                        initial_data[item]['thresholds']['comfort_range']['t_C']['min'] = patients['thresholds']['comfort_range']['t_C']['min']
                        initial_data[item]['thresholds']['comfort_range']['t_C']['max'] = patients['thresholds']['comfort_range']['t_C']['max']
                        initial_data[item]['thresholds']['comfort_range']['t_F']['u'] = patients['thresholds']['comfort_range']['t_F']['u']
                        initial_data[item]['thresholds']['comfort_range']['t_F']['min'] = patients['thresholds']['comfort_range']['t_F']['min']
                        initial_data[item]['thresholds']['comfort_range']['t_F']['max'] = patients['thresholds']['comfort_range']['t_F']['max']
                        initial_data[item]['thresholds']['comfort_range']['hum']['u'] = patients['thresholds']['comfort_range']['hum']['u']
                        initial_data[item]['thresholds']['comfort_range']['hum']['type'] = patients['thresholds']['comfort_range']['hum']['type']
                        initial_data[item]['thresholds']['comfort_range']['hum']['min'] = patients['thresholds']['comfort_range']['hum']['min']
                        initial_data[item]['thresholds']['comfort_range']['hum']['max'] = patients['thresholds']['comfort_range']['hum']['max']
                        print("\n")
                        print("Updating...")
                        time.sleep(1)
                        print("The file 'data.json' is updated:\nThe new {} of the {} is {}".format(key, item, initial_data[item]['thresholds']))
                        print('at time: {}'.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
                        print("\n\n")

                    else:
                        temp_json = {
                            "hr": {"u": patients['thresholds']['hr']['u'],
                                   "min": patients['thresholds']['hr']['min'],
                                   "max": patients['thresholds']['hr']['max']},
                            "bp": {"u": patients["thresholds"]["bp"]["u"],
                                   "normal": {"diastolic": {"min": patients['thresholds']['bp']['normal']['diastolic'],
                                                            "max": patients['thresholds']['bp']['normal']['diastolic']},
                                              "systolic": {"min": patients['thresholds']['bp']['normal']['systolic'],
                                                           "max": patients['thresholds']['bp']['normal']['systolic']}
                                              },
                                   "high": {"diastolic": {"min": patients['thresholds']['bp']['high']['diastolic'],
                                                          "max": patients['thresholds']['bp']['high']['diastolic']},
                                            "systolic": {"min": patients['thresholds']['bp']['high']['systolic'],
                                                         "max": patients['thresholds']['bp']['high']['systolic']}
                                            },
                                   "very_high": {
                                       "diastolic": {"min": patients['thresholds']['bp']['very_high']['diastolic'],
                                                     "max": patients['thresholds']['bp']['very_high']['diastolic']},
                                       "systolic": {"min": patients['thresholds']['bp']['very_high']['systolic'],
                                                    "max": patients['thresholds']['bp']['very_high']['systolic']}
                                   },
                                   "dangerous": {
                                       "diastolic": {"min": patients['thresholds']['bp']['dangerous']['diastolic'],
                                                     "max": patients['thresholds']['bp']['dangerous']['diastolic']},
                                       "systolic": {"min": patients['thresholds']['bp']['dangerous']['systolic'],
                                                    "max": patients['thresholds']['bp']['dangerous']['systolic']}
                                   }
                                   },
                            "hypoxemia": {"u": patients["thresholds"]["hypoxemia"]["u"],
                                          "slight": {"min": patients['thresholds']['hypoxemia']['slight']['min'],
                                                     "max": patients['thresholds']['hypoxemia']['slight']['max']},
                                          "moderate": {"min": patients['thresholds']['hypoxemia']['moderate']['min'],
                                                       "max": patients['thresholds']['hypoxemia']['moderate']['max']},
                                          "serious": {"min": patients['thresholds']['hypoxemia']['serious']['min'],
                                                      "max": patients['thresholds']['hypoxemia']['serious']['max']}},
                            "breathing_rate": {"u": patients["thresholds"]["breathing_rate"]["u"],
                                               "min": patients['thresholds']['breathing_rate']['min'],
                                               "max": patients['thresholds']['breathing_rate']['max']},
                            "temperature": {"u": patients["thresholds"]["temperature"]["u"],
                                            "freezing": {
                                                "min": patients['thresholds']['temperature']['freezing']["min"],
                                                "max": patients['thresholds']['temperature']['freezing']['max']
                                            },
                                            "very_cold": {
                                                "min": patients['thresholds']['temperature']['very_cold']["min"],
                                                "max": patients['thresholds']['temperature']['very_cold']['max']
                                            },
                                            "cold": {
                                                "min": patients['thresholds']['temperature']['cold']["min"],
                                                "max": patients['thresholds']['temperature']['cold']['max']
                                            },
                                            "comfort": {
                                                "min": patients['thresholds']['temperature']['comfort']["min"],
                                                "max": patients['thresholds']['temperature']['comfort']['max']
                                            },
                                            "warm": {
                                                "min": patients['thresholds']['temperature']['warm']["min"],
                                                "max": patients['thresholds']['temperature']['warm']['max']
                                            },
                                            "very_warm": {
                                                "min": patients['thresholds']['temperature']['very_warm']["min"],
                                                "max": patients['thresholds']['temperature']['very_warm']['max']
                                            },
                                            "boil": {
                                                "min": patients['thresholds']['temperature']['boil']["min"],
                                                "max": patients['thresholds']['temperature']['boil']['max']
                                            }
                                            },
                            "glucose_levels": {
                                "u": patients["thresholds"]["glucose_levels"]["u"],
                                "very_low": {
                                    "min": patients['thresholds']['glucose_levels']['very_low']["min"],
                                    "max": patients['thresholds']['glucose_levels']['very_low']["max"]
                                },
                                "low": {
                                    "min": patients['thresholds']['glucose_levels']['low']["min"],
                                    "max": patients['thresholds']['glucose_levels']['low']["max"]
                                },
                                "normal": {
                                    "min": patients['thresholds']['glucose_levels']['normal']["min"],
                                    "max": patients['thresholds']['glucose_levels']['normal']["max"]
                                },
                                "high": {
                                    "min": patients['thresholds']['glucose_levels']['high']["min"],
                                    "max": patients['thresholds']['glucose_levels']['high']["max"]
                                },
                                "very_high": {
                                    "min": patients['thresholds']['glucose_levels']['very_high']["min"],
                                    "max": patients['thresholds']['glucose_levels']['very_high']["max"]
                                }
                            },
                            "comfort_range": {
                                "t_C": {
                                    "min": patients['thresholds']['comfort_range']['t_C']["min"],
                                    "max": patients['thresholds']['comfort_range']['t_C']["max"],
                                    "u": patients["thresholds"]["comfort_range"]['t_C']["u"]
                                },
                                "t_F": {
                                    "min": patients['thresholds']['comfort_range']['t_F']["min"],
                                    "max": patients['thresholds']['comfort_range']['t_F']["max"],
                                    "u": patients["thresholds"]["comfort_range"]['t_F']["u"]
                                },
                                "hum": {
                                    "min": patients['thresholds']['comfort_range']['hum']["min"],
                                    "max": patients['thresholds']['comfort_range']['hum']["max"],
                                    "type": patients["thresholds"]["comfort_range"]['hum']["type"],
                                    "u": patients["thresholds"]["comfort_range"]['hum']["u"]
                                }
                            }
                        }
                        initial_data[item]['thresholds'] = temp_json
                        print("\n")
                        print("Updating...")
                        time.sleep(1)
                        print("The file 'data.json' is updated:\nThe new {} of the {} is {}".format(key, item, temp_json))
                        print('at time: {}'.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
                        print("\n\n")
                else:
                    temp_json = {item: {
                        "hr": {"u": patients['thresholds']['hr']['u'],
                               "min": patients['thresholds']['hr']['min'],
                               "max": patients['thresholds']['hr']['max']},
                        "bp": {"u": patietns["thresholds"]["bp"]["u"],
                               "normal": {"diastolic": {"min": patients['thresholds']['bp']['normal']['diastolic'],
                                                        "max": patients['thresholds']['bp']['normal']['diastolic']},
                                          "systolic": {"min": patients['thresholds']['bp']['normal']['systolic'],
                                                       "max": patients['thresholds']['bp']['normal']['systolic']}
                                          },
                               "high": {"diastolic": {"min": patients['thresholds']['bp']['high']['diastolic'],
                                                      "max": patients['thresholds']['bp']['high']['diastolic']},
                                        "systolic": {"min": patients['thresholds']['bp']['high']['systolic'],
                                                     "max": patients['thresholds']['bp']['high']['systolic']}
                                        },
                               "very_high": {
                                   "diastolic": {"min": patients['thresholds']['bp']['very_high']['diastolic'],
                                                 "max": patients['thresholds']['bp']['very_high']['diastolic']},
                                   "systolic": {"min": patients['thresholds']['bp']['very_high']['systolic'],
                                                "max": patients['thresholds']['bp']['very_high']['systolic']}
                               },
                               "dangerous": {
                                   "diastolic": {"min": patients['thresholds']['bp']['dangerous']['diastolic'],
                                                 "max": patients['thresholds']['bp']['dangerous']['diastolic']},
                                   "systolic": {"min": patients['thresholds']['bp']['dangerous']['systolic'],
                                                "max": patients['thresholds']['bp']['dangerous']['systolic']}
                               }
                               },
                        "hypoxemia": {"u": patietns["thresholds"]["hypoxemia"]["u"],
                                      "slight": {"min": patients['thresholds']['hypoxemia']['slight']['min'],
                                                 "max": patients['thresholds']['hypoxemia']['slight']['max']},
                                      "moderate": {"min": patients['thresholds']['hypoxemia']['moderate']['min'],
                                                   "max": patients['thresholds']['hypoxemia']['moderate']['max']},
                                      "serious": {"min": patients['thresholds']['hypoxemia']['serious']['min'],
                                                  "max": patients['thresholds']['hypoxemia']['serious']['max']}},
                        "breathing_rate": {"u": patietns["thresholds"]["breathing_rate"]["u"],
                                           "min": patients['thresholds']['breathing_rate']['min'],
                                           "max": patients['thresholds']['breathing_rate']['max']},
                        "temperature": {"u": patietns["thresholds"]["temperature"]["u"],
                                        "freezing": {
                                            "min": patients['thresholds']['temperature']['freezing']["min"],
                                            "max": patients['thresholds']['temperature']['freezing']['max']
                                        },
                                        "very_cold": {
                                            "min": patients['thresholds']['temperature']['very_cold']["min"],
                                            "max": patients['thresholds']['temperature']['very_cold']['max']
                                        },
                                        "cold": {
                                            "min": patients['thresholds']['temperature']['cold']["min"],
                                            "max": patients['thresholds']['temperature']['cold']['max']
                                        },
                                        "comfort": {
                                            "min": patients['thresholds']['temperature']['comfort']["min"],
                                            "max": patients['thresholds']['temperature']['comfort']['max']
                                        },
                                        "warm": {
                                            "min": patients['thresholds']['temperature']['warm']["min"],
                                            "max": patients['thresholds']['temperature']['warm']['max']
                                        },
                                        "very_warm": {
                                            "min": patients['thresholds']['temperature']['very_warm']["min"],
                                            "max": patients['thresholds']['temperature']['very_warm']['max']
                                        },
                                        "boil": {
                                            "min": patients['thresholds']['temperature']['boil']["min"],
                                            "max": patients['thresholds']['temperature']['boil']['max']
                                        }
                                        },
                        "glucose_levels": {
                            "u": patietns["thresholds"]["glucose_levels"]["u"],
                            "very_low": {
                                "min": patients['thresholds']['glucose_levels']['very_low']["min"],
                                "max": patients['thresholds']['glucose_levels']['very_low']["max"]
                            },
                            "low": {
                                "min": patients['thresholds']['glucose_levels']['low']["min"],
                                "max": patients['thresholds']['glucose_levels']['low']["max"]
                            },
                            "normal": {
                                "min": patients['thresholds']['glucose_levels']['normal']["min"],
                                "max": patients['thresholds']['glucose_levels']['normal']["max"]
                            },
                            "high": {
                                "min": patients['thresholds']['glucose_levels']['high']["min"],
                                "max": patients['thresholds']['glucose_levels']['high']["max"]
                            },
                            "very_high": {
                                "min": patients['thresholds']['glucose_levels']['very_high']["min"],
                                "max": patients['thresholds']['glucose_levels']['very_high']["max"]
                            }
                        },
                        "comfort_range": {
                            "t_C": {
                                "min": patients['thresholds']['comfort_range']['t_C']["min"],
                                "max": patients['thresholds']['comfort_range']['t_C']["max"],
                                "u": patietns["thresholds"]["comfort_range"]['t_C']["u"]
                            },
                            "t_F": {
                                "min": patients['thresholds']['comfort_range']['t_F']["min"],
                                "max": patients['thresholds']['comfort_range']['t_F']["max"],
                                "u": patietns["thresholds"]["comfort_range"]['t_F']["u"]
                            },
                            "hum": {
                                "min": patients['thresholds']['comfort_range']['hum']["min"],
                                "max": patients['thresholds']['comfort_range']['hum']["max"],
                                "type": patietns["thresholds"]["comfort_range"]['hum']["type"],
                                "u": patietns["thresholds"]["comfort_range"]['hum']["u"]
                            }
                        }
                    }}
                    initial_data.update(temp_json)
                    print("\n")
                    print("Updating...")
                    time.sleep(1)
                    print("The file 'data.json' is updated:\nThe new patient is posted!\nThe new {} of the {} is {}".format(key, item, temp_json))
                    print('at time: {}'.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
                    print("\n\n")

            elif key == 'Broker':
                initial_data['Broker']['Broker_IP'] = patients['Broker']['Broker_IP']
                initial_data['Broker']['Broker_port'] = patients['Broker']['Broker_port']
                print("\n")
                print("Updating...")
                time.sleep(1)
                print("The file 'data.json' is updated:\nThe new {} are :\nHost-IP: {}\nPort: {}".format(key, initial_data['Broker']['Broker_IP'], initial_data['Broker']['Broker_port']))
                print('at time: {}'.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
                print("\n\n")

            elif key == 'Telegram_bot':
                initial_data['Telegram_bot']['Port'] = patients['Telegram_bot']['Port']
                initial_data['Telegram_bot']['ID'] = patients['Telegram_bot']['ID']
                print("\n")
                print("Updating...")
                time.sleep(1)
                print("The file 'data.json' is updated:\nThe new {} are :\nPort: {}\nID: {}".format(key, initial_data['Telegram_bot']['Port'], initial_data['Telegram_bot']['ID']))
                print('at time: {}'.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
                print("\n\n")

            elif key == 'Data_for_Rest':
                initial_data['Data_for_Rest']['Host_IP'] = patients['Data_for_Rest']['Host_IP']
                initial_data['Data_for_Rest']['port'] = patients['Data_for_Rest']['port']
                print("\n")
                print("Updating...")
                time.sleep(1)
                print("The file 'data.json' is updated:\nThe new {} are :\nHost-IP: {}\nPort: {}".format(key, initial_data['Data_for_Rest']['Host_IP'], initial_data['Data_for_Rest']['port']))
                print('at time: {}'.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
                print("\n\n")

            initial_data['Date_time'] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            with open('data.json', 'w') as file:
                json.dump(initial_data, file)
                file.close()
            return "UPDATED!!!!"
        except Exception as e:
                print("ERROR IN POST: PROBLEM OF THE UPDATING DATA.JSON: ", e)


    def PUT(self):
        pass

    def DELETE(self):
        pass



if __name__ == '__main__':
    with  open("config_file.json", "r") as f:
        data = json.loads(f.read())
        f.close()
    IP = data["sourceCatalog"]["IP"]
    port = data["sourceCatalog"]["port"]

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True
        }
    }
    cherrypy.tree.mount(SourceCatalog(), '/', conf)

    cherrypy.config.update({'server.socket_host': str(IP)})
    cherrypy.config.update({'server.socket_port': int(port)})
    cherrypy.engine.start()
    cherrypy.engine.block()
