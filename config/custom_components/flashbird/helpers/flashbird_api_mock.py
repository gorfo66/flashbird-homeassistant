import logging
from ..const import EVT_NEED_REFRESH

_LOGGER = logging.getLogger(__name__)
API_URL = "https://pegase.api-smt.ovh/graphql"

def flashbird_get_token(login: str, password: str) -> str:
    _LOGGER.info('[mock] Get new token')
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJlNzhiNDlkNS05MjEyLTRmNmUtYTY3Ny0wMGFmMWEwMjNkOTUiLCJhZG1pbk1vZGUiOmZhbHNlLCJzZXNzaW9uIjpudWxsLCJyZXNldFBhc3N3b3JkQ29kZSI6bnVsbCwiaWF0IjoxNzI5NDQwMjYxLCJleHAiOjE3NjA5NzYyNjF9.XHpnmE9Mpt5VAspQEDD-T_diSfy9tKXzmsfSN3N85GM"


def flashbird_find_device_id(token, serial):
    _LOGGER.info('[mock] Find device id from serial ' + serial)
    return "c240ead8-51b3-45f3-aa28-74ba01c9622f"


def flashbird_get_device_info(token, device_id):
    _LOGGER.info('[mock] Find device info from id ' + device_id)
    return {
                "id": "c240ead8-51b3-45f3-aa28-74ba01c9622f",
                "activated": True,
                "latitude": 43.645573,
                "longitude": 6.929856,
                "lockEnabled": True,
                "deviceType": "FLASHBIRD",
                "serialNumber": "F111F26PMKDES7P6",
                "batteryPercentage": 100,
                "status": {
                    "isConnectedToGSM": True,
                    "lastPollingTimestamp": 1729357818507
                },
                "motorcycle": {
                    "id": "a38ca81a-3d04-4d24-8383-1583d2339de4",
                    "brand": {
                        "label": "Yamaha"
                    },
                    "model": {
                        "label": "MT09"
                    }
                },
                "statistics": {
                    "totalDistance": 658839,
                    "totalTime": 60493000
                }
            }

def flashbird_set_lock_enabled(token, device_id, status, callback):
    _LOGGER.info('Change lock status ' + device_id)
    if callback:
        callback()
