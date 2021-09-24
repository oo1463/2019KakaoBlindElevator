import json
import requests

from API.X_auth_token import *

base_url = Base_url
user_key = User_key


class Api:
    @staticmethod
    def get_auth_token(problem, num_of_elevators):
        url = f'{base_url}/start/{user_key}/{problem}/{num_of_elevators}'
        try:
            response_start = requests.post(url).json()
        except:
            return None
        return response_start

    @staticmethod
    def oncall(auth_token):
        url = f'{base_url}/oncalls'
        headers = {'X-Auth-Token': auth_token}
        try:
            res_oncall = requests.get(url, headers=headers).json()
        except:
            return None
        return res_oncall

    @staticmethod
    def action(auth_token, commands):
        url = f'{base_url}/action'
        headers = {'Content-Type': 'application/json; charset=utf-8', 'X-Auth-Token': auth_token}

        try:
            res_action = requests.post(url, headers=headers, json={"commands": commands}).json()
        except:
            return None
        return res_action
