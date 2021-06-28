import requests
import json

class Qapitan:

    QAPITAN_PUBLIC_API= "https://hpg6m6hw7c.execute-api.eu-west-3.amazonaws.com/dev"
    PAYLOAD_USER = {'username': 'adrian@qapitan.com', 'password': 'qapified'}

    def __init__(self, QAPITAN_PUBLIC_API = False, PAYLOAD_USER = False):
        self.QAPITAN_PUBlIC_API = QAPITAN_PUBLIC_API
        self.PAYLOAD_USER = PAYLOAD_USER

    def login(self):
        response = requests.post(self.QAPITAN_PUBLIC_API + '/login', data=json.dumps(self.PAYLOAD_USER))
        print(self.PAYLOAD_USER)
        print(self.QAPITAN_PUBLIC_API)
        print(response)
        response_json = response.json()
        
        access_token = response_json['access_token']
        header = {'Authorization': 'Bearer ' + access_token}
        return header

    def qapitan_api_execute(self, problem, payload):
        header = self.login()
        response = requests.post(self.QAPITAN_PUBLIC_API + '/problem/' + problem, data=json.dumps(payload), headers=header)
        response_json = response.json()
        return response_json['job']

    def get_result(self, job_name):
        header = self.login()
        response = requests.get(self.QAPITAN_PUBLIC_API + "/results", headers=header)
        return response.json()