from homeassistant.const import Platform

REFRESH_RATE = 10

DOMAIN = "Flashbird"
PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.DEVICE_TRACKER,
    Platform.LOCK,
]

CONF_SERIAL_NUMBER = "serial"
CONF_TOKEN = "token"
CONF_TRACKER_ID = "trackerId"
CONF_MANUFACTURER = "manufacturer"
CONF_MODEL = "model"
CONF_FIRMWARE_VERSION = "firmwareVersion"
CONF_NAME = "name"

EVT_DEVICE_INFO_RETRIEVED = "event_device_info_retrieved"
EVT_NEED_REFRESH = "event_device_info_need_refresh"
