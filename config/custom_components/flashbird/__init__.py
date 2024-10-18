"""Initialisation du package de l'intégration HACS Tuto"""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, PLATFORMS
from .helpers.flashbird_api import flashbird_get_token, flashbird_get_device_info

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Creation des entités à partir d'une configEntry"""

    _LOGGER.debug(
        "Appel de async_setup_entry entry: entry_id='%s', data='%s'",
        entry.entry_id,
        entry.data,
    )

    hass.data.setdefault(DOMAIN, {})

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    token = await hass.async_add_executor_job(flashbird_get_token, 'frog@gorfo.com', "MG&4vvY6eXPs$vkpCFm5")
    deviceInfo = await hass.async_add_executor_job(flashbird_get_device_info, token, "c240ead8-51b3-45f3-aa28-74ba01c9622f")
    _LOGGER.debug(deviceInfo)

    return True
