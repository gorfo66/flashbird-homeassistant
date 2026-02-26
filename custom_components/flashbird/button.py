"""Instantiate button entities for Flashbird integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.flashbird.entities.maintenance_counter_chain_reset_button_entity import (
    FlashbirdMaintenanceCounterChainResetButtonEntity,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Do the setup for the button entities."""
    _LOGGER.debug("Calling async_setup_entry (button) entry=%s", entry.entry_id)

    async_add_entities(
        [FlashbirdMaintenanceCounterChainResetButtonEntity(hass, entry)],
        update_before_add=False,
    )
