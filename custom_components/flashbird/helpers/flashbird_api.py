"""API client for Flashbird device communication."""

import logging

import requests

from .flashbird_device_info import FlashbirdDeviceInfo

_LOGGER = logging.getLogger(__name__)
API_URL = "https://pegase.api-smt.ovh/graphql"
INVALID_TOKEN_MSG = "invalid token"  # noqa: S105
TIMEOUT = 10


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

    r = requests.post(API_URL, json=payload, timeout=TIMEOUT)

    response = r.json()

    if "errors" in response:
        _LOGGER.error("The authentication failed")
        raise ValueError(INVALID_TOKEN_MSG)

    return response["data"]["createUserOrSignInWithEmailAndPassword"]["token"]


def flashbird_find_device_id(token: str, serial: str) -> str:
    """Find device id from the serial number."""
    _LOGGER.info("Find device id from serial %s", serial)
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
    r = requests.post(API_URL, json=payload, headers=headers, timeout=TIMEOUT)
    response = r.json()

    if "errors" in response:
        _LOGGER.error(INVALID_TOKEN_MSG)
        raise ValueError(INVALID_TOKEN_MSG)

    for device in response["data"]["user"]["devices"]:
        if device["serialNumber"] == serial:
            return device["id"]

    return None


def flashbird_get_device_info(token: str, device_id: str) -> FlashbirdDeviceInfo:
    """Get device information from API."""
    _LOGGER.info("Find device info from id %s", device_id)
    payload = {
        "operationName": "Devices",
        "query": """
          query Devices($deviceId: ID!) {
            user {
              device(id: $deviceId) {
                id
                softVersion
                latitude
                longitude
                lockEnabled
                deviceType
                serialNumber
                batteryPercentage
                status {
                  isConnectedToGSM
                }
                motorcycle {
                  brand {
                    label
                  }
                  model {
                    label
                  }
                  batteryVoltageInMillivolt
                }
                statistics {
                  totalDistance
                  totalTime
                }
                smartKeys {
                  serialNumber
                  batteryPercentage
                }
                lockEventTimestamp
                lockEventConnection {
                  edges {
                    node {
                      id
                      level
                      timestamp
                    }
                  }
                }
              }
            }
          }
        """,
        "variables": {"deviceId": device_id},
    }
    headers = {"Authorization": "Bearer " + token}
    r = requests.post(API_URL, json=payload, headers=headers, timeout=TIMEOUT)
    response = r.json()

    if "errors" in response:
        _LOGGER.error(INVALID_TOKEN_MSG)
        raise ValueError(INVALID_TOKEN_MSG)

    data = response["data"]["user"]["device"]
    _LOGGER.debug(data)
    return FlashbirdDeviceInfo(data)


def flashbird_set_lock_enabled(token: str, device_id: str, status: bool) -> None:
    """Set lock status for the device."""
    _LOGGER.info("Change lock status %s", device_id)
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
    requests.post(API_URL, json=payload, headers=headers, timeout=TIMEOUT)
