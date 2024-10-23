"""Initialisation du package de l'intégration HACS Tuto"""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.loader import async_get_loaded_integration

from .const import DOMAIN, EVT_NEED_REFRESH, PLATFORMS
from .coordinator import FlashbirdDataUpdateCoordinator
from .data import FlashbirdData


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug(
        "Appel de async_setup_entry entry: entry_id='%s', data='%s'",
        entry.entry_id,
        entry.data,
    )

    hass.data.setdefault(DOMAIN, {})


    entry.runtime_data = FlashbirdData(
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    coordinator = FlashbirdDataUpdateCoordinator(hass = hass)
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    # hass.bus.fire(EVT_NEED_REFRESH)
    return True
