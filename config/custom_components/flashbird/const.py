from homeassistant.const import Platform

REFRESH_RATE = 30

DOMAIN = "flashbird"
PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.DEVICE_TRACKER]

CONF_SERIAL_NUMBER = "serial"
CONF_TOKEN = "token"
CONF_TRACKER_ID = "trackerId"
CONF_MANUFACTURER = "manufacturer"
CONF_MODEL = "model"

EVT_DEVICE_INFO_RETRIEVED = "event_device_info_retrieved"