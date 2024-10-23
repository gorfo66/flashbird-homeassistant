import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entities.flashbird_tracker_entity import FlashbirdTrackerEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Do the setup all the tracker entities."""
    _LOGGER.debug("Calling async_setup_entry entry=%s", entry)

    async_add_entities([FlashbirdTrackerEntity(hass, entry)], update_before_add=True)
