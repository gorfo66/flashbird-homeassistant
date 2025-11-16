"""API client for Flashbird device communication."""

import logging

import requests

from .flashbird_device_info import FlashbirdDeviceInfo

_LOGGER = logging.getLogger(__name__)
API_URL = "https://pegase.api-smt.ovh/graphql"


def flashbird_get_token(login: str, password: str) -> str:
    """Get authentication token from API."""
    _LOGGER.info("Get new token")
    payload = {
        "query": """
          mutation CreateUserOrSignInWithEmailAndPassword($email: String!, $password: String!) {
            createUserOrSignInWithEmailAndPassword(email: $email, password: $password) {
              token
            }
          }
        """,
        "variables": {"email": login, "password": password},
        "operationName": "CreateUserOrSignInWithEmailAndPassword",
    }

    r = requests.post(API_URL, json=payload)

    response = r.json()

    if "errors" in response:
        _LOGGER.error("The authentication failed")
        raise ValueError("invalid credentials")

    return response["data"]["createUserOrSignInWithEmailAndPassword"]["token"]


def flashbird_find_device_id(token: str, serial: str) -> str:
    """Find device id from the serial number."""
    _LOGGER.info("Find device id from serial " + serial)
    payload = {
        "operationName": "Devices",
        "query": """
          query Devices {
            user {
              devices {
                id
                serialNumber
              }
            }
          }
        """,
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


def flashbird_get_device_info(token: str, device_id: str) -> FlashbirdDeviceInfo:
    """Get device information from API."""
    _LOGGER.info("Find device info from id " + device_id)
    payload = {
        "operationName": "Devices",
        "query": """
            query Devices($deviceId: ID!) {
              user {
                device(id: $deviceId) {
                  id softVersion latitude longitude lockEnabled
                  deviceType serialNumber batteryPercentage
                  status { isConnectedToGSM lastPollingTimestamp }
                  motorcycle {
                    brand { label }
                    model { label }
                    batteryVoltageInMillivolt
                  }
                  statistics { totalDistance totalTime }
                  smartKeys { serialNumber batteryPercentage }
                }
              }
            }
          """,
        "variables": {"deviceId": device_id},
    }
    headers = {"Authorization": "Bearer " + token}
    r = requests.post(API_URL, json=payload, headers=headers)
    response = r.json()

    if "errors" in response:
        _LOGGER.error("Token expired")
        raise ValueError("invalid token")

    data = response["data"]["user"]["device"]
    _LOGGER.debug(data)
    return FlashbirdDeviceInfo(data)


def flashbird_set_lock_enabled(token: str, device_id: str, status: bool) -> None:
    """Set lock status for the device."""
    _LOGGER.info("Change lock status " + device_id)
    payload = {
        "operationName": "SetLockEnabled",
        "query": """
          mutation SetLockEnabled($enabled: Boolean!, $deviceId: String) {
            setLockEnabled(enabled: $enabled, deviceId: $deviceId)
          }
        """,
        "variables": {"enabled": status, "deviceId": device_id},
    }

    headers = {"Authorization": "Bearer " + token}
    requests.post(API_URL, json=payload, headers=headers)
