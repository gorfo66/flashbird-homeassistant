import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .entities.flashbird_lock_entity import FlashbirdLockEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
):

    _LOGGER.debug("Calling async_setup_entry entry=%s", entry)

    async_add_entities([
        FlashbirdLockEntity(hass, entry),
    ], True)
