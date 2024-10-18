import logging
import requests
import json
from ..const import API_URL

_LOGGER = logging.getLogger(__name__)


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


def flashbird_get_device_info(token, device_id):
    payload = {"query": "query Devices {  user {    devices {      id      activated      latitude      longitude      lockEnabled      deviceType      orientation      serialNumber      vehicleType      batteryPercentage      status {        isConnectedToGSM        lastPollingTimestamp      }      statistics {        totalDistance      }      motorcycle {        id        brand {          label        }        model {          label        }      }      statistics {        totalDistance        totalTime      }    }  }}", "variables": {}, "operationName": "Devices"}
    headers = {'Authorization': 'Bearer ' + token}
    r = requests.post(API_URL, json=payload, headers=headers)
    response = r.json()
    for device in response['data']['user']['devices']:
        if device['id'] == device_id:
            return device

    return None
