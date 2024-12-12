from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo

from ..const import *


def define_device_info(configEntry: ConfigEntry) -> DeviceInfo:
    device = DeviceInfo(
        entry_type=None,
        identifiers={(DOMAIN, configEntry.entry_id)},
        name=configEntry.data[CONF_SERIAL_NUMBER],
        #manufacturer=configEntry.data[CONF_MANUFACTURER],
        manufacturer="SMT Performances",
        #model=configEntry.data[CONF_MODEL],
        model="Flashbird",
        serial_number=configEntry.data[CONF_SERIAL_NUMBER]
    )

    # todo: on fresh installation directly do from the name and not from the serial
    if CONF_NAME in configEntry.data:
        device.update(name=configEntry.data[CONF_NAME])

    if CONF_FIRMWARE_VERSION in configEntry.data:
        device.update(sw_version=configEntry.data[CONF_FIRMWARE_VERSION])

    return device



def define_device_info_key(configEntry: ConfigEntry) -> DeviceInfo:
    device = DeviceInfo(
        entry_type=None,
        identifiers={(DOMAIN, configEntry.entry_id + '_key')},
        name=configEntry.data[CONF_NAME] + ' Smart key',
        manufacturer="SMT Performances",
        model="SmartKey"
    )

    # add the serial number if present in the configuration (not available in first boot)
    if CONF_SERIAL_NUMBER_KEY in configEntry.data:
        device.update(serial_number=configEntry.data[CONF_SERIAL_NUMBER_KEY])

    return device