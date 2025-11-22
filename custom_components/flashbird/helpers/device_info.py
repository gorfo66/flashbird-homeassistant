"""Helper module for device info definitions."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo

from custom_components.flashbird.const import (
    CONF_FIRMWARE_VERSION,
    CONF_MODEL,
    CONF_NAME,
    CONF_SERIAL_NUMBER,
    CONF_SERIAL_NUMBER_KEY,
    DOMAIN,
)


def define_device_info(config_entry: ConfigEntry) -> DeviceInfo:
    """Define device info for the Flashbird device."""
    device = DeviceInfo(
        entry_type=None,
        identifiers={(DOMAIN, config_entry.entry_id)},
        name=config_entry.data[CONF_SERIAL_NUMBER],
        manufacturer="SMT Performances",
        model=config_entry.data[CONF_MODEL],
        serial_number=config_entry.data[CONF_SERIAL_NUMBER],
    )

    if CONF_NAME in config_entry.data:
        device.update(name=config_entry.data[CONF_NAME])

    if CONF_FIRMWARE_VERSION in config_entry.data:
        device.update(sw_version=config_entry.data[CONF_FIRMWARE_VERSION])

    return device


def define_device_info_key(config_entry: ConfigEntry) -> DeviceInfo:
    """Define device info for the Flashbird smart key."""
    device = DeviceInfo(
        entry_type=None,
        identifiers={(DOMAIN, config_entry.entry_id + "_key")},
        name=config_entry.data[CONF_NAME] + " Smart key",
        manufacturer="SMT Performances",
        model="SmartKey",
    )

    # add the serial number if present in the configuration (not available in first boot)
    if CONF_SERIAL_NUMBER_KEY in config_entry.data:
        device.update(serial_number=config_entry.data[CONF_SERIAL_NUMBER_KEY])

    return device
