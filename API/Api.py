import json
import requests

from API.X_auth_token import *

base_url = Base_url
user_key = User_key


class Api:
    def get_auth_token(problem, num_of_elevators):
        url = base_url + '/' + 'start/' + user_key + '/' + str(problem) + '/' + str(num_of_elevators)
        try:
            response_start = requests.post(url).json()
        except:
            return None
        return response_start

    def oncall(auth_token):
        url = base_url + '/' + 'oncalls'
        headers = {'X-Auth-Token': auth_token}
        try:
            res_oncall = requests.get(url, headers=headers).json()
        except:
            return None
        return res_oncall

    def action(auth_token, commands):
        url = base_url + '/' + 'action'
        headers = {'Content-Type': 'application/json; charset=utf-8', 'X-Auth-Token': auth_token}

        # res_action = requests.post(url, headers=headers, json={"commands": commands}).json()
        try:
            res_action = requests.post(url, headers=headers, json={"commands": commands}).json()
        except:
            return None
        return res_action
