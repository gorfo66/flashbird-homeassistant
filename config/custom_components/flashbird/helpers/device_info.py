from homeassistant.helpers.entity import DeviceInfo
from homeassistant.config_entries import ConfigEntry
from ..const import *

def define_device_info(configEntry: ConfigEntry) -> DeviceInfo :
  return DeviceInfo(
    entry_type=None,
    identifiers={(DOMAIN, configEntry.entry_id)},
    name=configEntry.data[CONF_SERIAL_NUMBER],
    manufacturer=configEntry.data[CONF_MANUFACTURER],
    model=configEntry.data[CONF_MODEL]
  )