import logging

import requests

_LOGGER = logging.getLogger(__name__)
API_URL = "https://pegase.api-smt.ovh/graphql"


def flashbird_get_token(login: str, password: str) -> str:
    _LOGGER.info("Get new token")
    payload = {
        "query": "mutation CreateUserOrSignInWithEmailAndPassword($email: String!, $password: String!) { createUserOrSignInWithEmailAndPassword(email: $email, password: $password) { token }}",
        "variables": {"email": login, "password": password},
        "operationName": "CreateUserOrSignInWithEmailAndPassword",
    }

    r = requests.post(API_URL, json=payload)

    response = r.json()

    if "errors" in response:
        _LOGGER.error("The authentication failed")
        raise ValueError("invalid credentials")

    return response["data"]["createUserOrSignInWithEmailAndPassword"]["token"]


def flashbird_find_device_id(token, serial) -> str:
    _LOGGER.info("Find device id from serial " + serial)
    payload = {
        "operationName": "Devices",
        "query": "query Devices { user { devices { id  serialNumber }}}",
        "variables": {},
    }
    headers = {"Authorization": "Bearer " + token}
    r = requests.post(API_URL, json=payload, headers=headers)
    response = r.json()

    if "errors" in response:
        _LOGGER.error("Token expired")
        raise ValueError("invalid token")

    for device in response["data"]["user"]["devices"]:
        if device["serialNumber"] == serial:
            return device["id"]

    return None


def flashbird_get_device_info(token, device_id):
    _LOGGER.info("Find device info from id " + device_id)
    payload = {
        "operationName": "Devices",
        "query": "query Devices($deviceId: ID!) { user { device(id: $deviceId) { id softVersion activated latitude longitude lockEnabled deviceType serialNumber batteryPercentage status { isConnectedToGSM lastPollingTimestamp } motorcycle { id brand { label } model { label } } statistics { totalDistance totalTime } } }}",
        "variables": {"deviceId": device_id},
    }
    headers = {"Authorization": "Bearer " + token}
    r = requests.post(API_URL, json=payload, headers=headers)
    response = r.json()

    if "errors" in response:
        _LOGGER.error("Token expired")
        raise ValueError("invalid token")

    return response["data"]["user"]["device"]


def flashbird_set_lock_enabled(token, device_id, status, callback):
    _LOGGER.info("Change lock status " + device_id)
    payload = {
        "operationName": "SetLockEnabled",
        "query": "mutation SetLockEnabled($enabled: Boolean!, $deviceId: String) { setLockEnabled(enabled: $enabled, deviceId: $deviceId)}",
        "variables": {"enabled": status, "deviceId": device_id},
    }

    headers = {"Authorization": "Bearer " + token}
    requests.post(API_URL, json=payload, headers=headers)

    if callback:
        callback()
