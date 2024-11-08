from homeassistant.const import Platform

REFRESH_RATE = 300

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
