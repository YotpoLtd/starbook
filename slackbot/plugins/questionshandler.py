from slackclient import SlackClient

import os
import pickle
import re
import requests
import json


def send_user_data_to_starbook(data):
    r = requests.post("http://" + os.environ['WEBSERVER_HOST'] + ":5000/add_person", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    print(print(r.status_code, r.reason))


outputs = []
crontabs = []

employees = {}

FILE = "plugins/employees.data"
if os.path.isfile(FILE):
    employees = pickle.load(open(FILE, 'rb'))


def process_message(data):
    if os.path.isfile(FILE):
        employees = pickle.load(open(FILE, 'rb'))
    slack_client = data['rtmbot'].slack_client
    channel = data["channel"]

    if channel not in employees.keys():
        channel = ""

    text = data["text"]
    # only accept tasks on DM channels
    if channel.startswith("D") and not data['rtmbot'].pluginssharedvars['isnewemployee']:
        # do command stuff
        employee = employees[channel]
        stage = employee['stage']

        if stage == 0:
            employee['stage'] += 1
            employee['fields']['name'] = text
            outputs.append([channel, "Wow, great name! Now please copy&paste a public link to an image of yours"])

        elif stage == 1:
            employee['stage'] += 1
            employee['fields']['image'] = re.sub('[\<\>]', '', text)
            outputs.append([channel, "What's the email of your direct manager? "])

        elif stage == 2:
            employee['stage'] += 1
            employee['fields']['boss'] = employee_email = re.findall(r"^.*:([a-zA-Z0-9]+@yotpo.com).*$", text)[0]
            outputs.append([channel, "nice, now, what is your role? "])

        elif stage == 3:
            employee['stage'] += 1
            employee['fields']['title'] = text
            outputs.append([channel,
                            "So, {} what are your personal hobbies/interests? (ex. Pizza, theater, sports, hot sauce)?".format(
                                employee['fields']['name'])])
        elif stage == 4:
            employee['stage'] += 1
            employee['fields']['hobbies'] = text.split(',')
            outputs.append([channel, "What are you pro at? (ex. css, adwords, excel, graphic design)"])
        elif stage == 5:
            employee['stage'] += 1
            employee['fields']['expertise'] = text.split(',')
            outputs.append(
                [channel, "What’s your ‘hood? (ex. williamsburg, east village, Florentine, kfar saba)"])
        elif stage == 6:
            employee['stage'] += 1
            employee['fields']['hood'] = text
            outputs.append([channel,
                            "Wow! There are 5 other employees who live in {} too! Now, what’s your Facebook profile URL?".format(
                                employee['fields']['hood'])])
        elif stage == 7:
            employee['stage'] += 1
            employee['fields']['facebook'] = text
            outputs.append([channel,
                            "Thanks! Okay, so you completed your profile. Check out the link below to see your profile and all of your new Yotpo family. See you soon!"])
            send_user_data_to_starbook(employee['fields'])

        pickle.dump(employees, open(FILE, "wb"))
