import requests
import json

class Qapitan:

    def __init__(self, QAPITAN_PUBLIC_API, PAYLOAD_USER):
        self.QAPITAN_PUBLIC_API = QAPITAN_PUBLIC_API
        self.PAYLOAD_USER = PAYLOAD_USER
        print(self.PAYLOAD_USER)

    def login(self):
        response = requests.post(self.QAPITAN_PUBLIC_API + '/login', json=self.PAYLOAD_USER)
        response_json = response.json()

        print(response_json)
        
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

    def get_best_result(self, header, job_name):
        result = self.get_result(header, job_name)
        for i in result['job'][job_name]['executions']:
            return result['job'][job_name]['executions'][i]['result']