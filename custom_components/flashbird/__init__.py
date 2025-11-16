"""Initialisation du package de l'intégration HACS Tuto"""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.loader import async_get_loaded_integration

from .const import DOMAIN, PLATFORMS
from .coordinator import FlashbirdDataUpdateCoordinator
from .data import FlashbirdData

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("async_setup_entry entry_id='%s'", entry.entry_id)

    hass.data.setdefault(DOMAIN, {})

    coordinator = FlashbirdDataUpdateCoordinator(hass=hass)
    entry.runtime_data = FlashbirdData(
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # force the refresh before creation of the sensors, to create the smart key only if available
    await coordinator.async_config_entry_first_refresh()

    # Create the sensors
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # force the refresh at initialization. To get data from the begining
    await coordinator.refresh_data()

    return True
