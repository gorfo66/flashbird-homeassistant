import logging
import requests

_LOGGER = logging.getLogger(__name__)
API_URL = "https://pegase.api-smt.ovh/graphql"

def flashbird_get_token(login: str, password: str) -> str:
    payload = {
        "query": "mutation CreateUserOrSignInWithEmailAndPassword($email: String!, $password: String!) { createUserOrSignInWithEmailAndPassword(email: $email, password: $password) { token }}",
        "variables": {
            "email": login,
            "password": password
        },
        "operationName": "CreateUserOrSignInWithEmailAndPassword"
    }

    r = requests.post(API_URL, json=payload)

    response = r.json()
    return response['data']['createUserOrSignInWithEmailAndPassword']['token']


def flashbird_find_device_id(token, serial):
    payload = {
        "operationName": "Devices",
        "query": "query Devices { user { devices { id  serialNumber }}}",
        "variables": {}
    }
    headers = {'Authorization': 'Bearer ' + token}
    r = requests.post(API_URL, json=payload, headers=headers)
    response = r.json()
    for device in response['data']['user']['devices']:
        if device['serialNumber'] == serial:
            return device['id']

    return None


def flashbird_get_device_info(token, device_id):
    payload = {
        "operationName": "Devices",
        "query": "query Devices($deviceId: ID!) { user { device(id: $deviceId) { id activated latitude longitude lockEnabled deviceType orientation serialNumber vehicleType batteryPercentage status { isConnectedToGSM lastPollingTimestamp } motorcycle { id brand { label } model { label } } statistics { totalDistance totalTime } } }}",
        "variables": {
            "deviceId": device_id
        }
    }
    headers = {'Authorization': 'Bearer ' + token}
    r = requests.post(API_URL, json=payload, headers=headers)
    response = r.json()
    return response['data']['user']['device']
