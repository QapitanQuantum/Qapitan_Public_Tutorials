import requests
import json


class Qapitan:
    QAPITAN_PUBLIC_API = "https://hpg6m6hw7c.execute-api.eu-west-3.amazonaws.com/dev"
    PAYLOAD_USER = {'username': 'adrian@qapitan.com', 'password': 'qapified'}

    def __init__(self, QAPITAN_PUBLIC_API=False, PAYLOAD_USER=False):
        self.QAPITAN_PUBlIC_API = QAPITAN_PUBLIC_API
        self.PAYLOAD_USER = PAYLOAD_USER

    def login(self):
        response = requests.post(self.QAPITAN_PUBLIC_API + '/login', json=self.PAYLOAD_USER)
        response_json = response.json()
        
        access_token = response_json['access_token']
        header = {'Authorization': 'Bearer ' + access_token}
        return header

    def execute(self, header, problem, payload):
        response = requests.post(self.QAPITAN_PUBLIC_API + '/problem/' + problem, json=payload, headers=header)
        response_json = response.json()
        return response_json

    def get_result(self, header, job_name):
        response = requests.get(self.QAPITAN_PUBLIC_API + "/job/" + job_name, headers=header)
        return response.json()

    def get_results(self, header):
        response = requests.get(self.QAPITAN_PUBLIC_API + "/results", headers=header)
        return response.json()
