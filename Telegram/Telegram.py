# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The Telegram.py script 
"""

import logging
import json
import requests
import os

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

INFORMATION, RETRIVER, OTHER = range(3)


class TelegramBot(object):

    def __init__(self, url, token, patients_list, patients_name, info_list):
        self.token = token
        self.url = url
        self.pat_list = patients_list
        self.pat_names = patients_name
        self.info_list = info_list

    def control(self, element, json_string):
        if type(json_string) == dict:
            string = []
            for key in json_string:
                string.append(key+" : "+str(json_string[key]))
        else:
            string = [element+" : "+json_string]
        return string

    def setWS(self):
        request = requests.get(self.url+"Data_for_Rest")
        dataRest = json.loads(request.text)
        self.urlRest = dataRest["Host_IP"]
        self.portRest = dataRest["port"]



    def start(self, update, context):
        self.setWS()
        patients = []
        for patient in self.pat_list:
            req_pat = requests.get("http://" + self.urlRest + ":" + str(self.portRest) + "/"+patient+"/all")
            pat_name = json.loads(req_pat.text)["Name"]
            pat_surname = json.loads(req_pat.text)["Surname"]
            pat = pat_name+' '+pat_surname+'-'+patient
            patients.append(pat)
        print(patients)
        update.message.reply_text(
            'Hi! My name is TelemediceBot and I will retrive you some information about your patients. '
            'Send /cancel to stop talking to me.\n\n'
            'Which patient would you monitoring?',
            reply_markup=ReplyKeyboardMarkup([patients], one_time_keyboard=True))

        return INFORMATION

    def information(self, update, context):
        user = update.message.from_user
        patient = update.message.text
        patient = patient.split('-')[1]
        request = requests.get("http://" + self.urlRest + ":" + str(self.portRest) + "/"+patient+"/all")
        # Getting the information list
        self.json_string = json.loads(request.text)

        information_list = list(self.json_string.keys())
        update.message.reply_text('Choose only one of the following information',
                                  reply_markup=ReplyKeyboardMarkup([information_list], one_time_keyboard=True))

        return RETRIVER

    def retriver(self, update, context):

        user = update.message.from_user

        self.command = update.message.text
        print(self.command)
        print(self.json_string[self.command])
        string = self.control(self.command, self.json_string[self.command])

        if len(string) > 1:
            for x in string:
                update.message.reply_text(x)
        else:
            update.message.reply_text(string[0])
        update.message.reply_text('If you want to restart the conversation, click /start\n'
                                  'If you want to end the conversation, click /end')

        return OTHER


    def cancel(self, update, context):
        user = update.message.from_user
        update.message.reply_text('Bye! I hope we can talk again some day.',
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    def main(self):
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        updater = Updater(self.token, use_context=True)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # Add conversation handler with the states INFORMATION, PHOTO, LOCATION and BIO
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],

            states={
                INFORMATION: [MessageHandler(Filters.regex('^('+'|'.join(map(str, self.pat_names))+')$'), self.information)],

                RETRIVER: [MessageHandler(Filters.regex(
                    '^('+'|'.join(map(str, self.info_list))+')$'),
                    self.retriver)],
            },

            fallbacks=[CommandHandler('end', self.cancel)],
            allow_reentry=True
        )

        dp.add_handler(conv_handler)

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()


if __name__ == '__main__':

    with open("config_file.json", "r") as file:
        json_string = file.read()
    file.close()
    config_json = json.loads(json_string)
    url = config_json["sourceCatalog"]["url"]
    patients_list = list(config_json["patients"].keys())

    info_list = list(json.loads(requests.get(url+patients_list[0]).text)['topic'].keys())
    patients_name = []
    for i in range(len(patients_list)):
        patients_name.append(list(config_json["patients"].values())[i]+'-'+patients_list[i])
    print(patients_name)
    while 'Clinical_situation' in info_list:
        info_list[info_list.index('Clinical_situation')] = 'id'

    request = requests.get(url+"Telegram_bot")
    telegram_info = json.loads(request.text)
    TOKEN = telegram_info["TOKEN"]


    Telegram_Bot = TelegramBot(url, TOKEN, patients_list, patients_name, info_list)
    Telegram_Bot.main()
