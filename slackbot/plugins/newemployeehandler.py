from slackclient import SlackClient

import os
import pickle
import re

outputs = []
crontabs = []

employees = {}

FILE = "plugins/employees.data"
pickle.dump(employees, open(FILE, "wb"))

def get_user_id_from_email(users, employee_email):
    for user in users:
            if user.get('profile').get('email') == employee_email:
                return user.get('id')
    else:
        print("could not find bot user with the email " + employee_email)
        return None


def email_to_slack_channel(employee_email, slack_client):

    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get('members')
        user_id = get_user_id_from_email(users, employee_email)
        return slack_client.api_call('im.open', user=user_id)['channel']['id']



def process_message(data):

    if os.path.isfile(FILE):
        employees = pickle.load(open(FILE, 'rb'))

    data['rtmbot'].pluginssharedvars['isnewemployee'] = False
    slack_client = data['rtmbot'].slack_client

    channel = data["channel"]
    text = data["text"]
    # only accept tasks on DM channels
    if channel.startswith("D"):

        # do command stuff
        if text.startswith("new employee"):
            data['rtmbot'].pluginssharedvars['isnewemployee'] = True
            employee_email = re.findall(r"^.*:([a-zA-Z0-9]+@yotpo.com).*$", text[12:])[0]
            new_employee_channel = email_to_slack_channel(employee_email, slack_client)


            employees[employee_email] = {}
            employees[employee_email]['channel'] = new_employee_channel
            employees[employee_email]['stage'] = 0
            employees[employee_email]['fields'] = {}
            employees[employee_email]['fields']['email'] = employee_email
            employees[new_employee_channel] = employees[employee_email]

            outputs.append([channel, "added"])

            #say hellow to new employee
            outputs.append([new_employee_channel, "Welcome to Yotpo. Glad to have you on board! I’m gonna ask you a few questions to get you set up in Starbook, our amazing social network.\nWhat do you like to be called?"]);
            pickle.dump(employees, open(FILE, "wb"))
