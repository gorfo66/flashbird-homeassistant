"""Instantiate binary sensor entities."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.flashbird.entities.is_connected_entity import (
    FlashbirdConnectedEntity,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Do the setup all the binary sensor entities."""
    _LOGGER.debug("Calling async_setup_entry entry=%s", entry.entry_id)

    async_add_entities(
        [
            FlashbirdConnectedEntity(hass, entry),
        ],
        update_before_add=False,
    )
