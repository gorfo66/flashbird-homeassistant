import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .entities.flashbird_refresh_entity import FlashbirdRefreshEntity
from .entities.flashbird_odometer_entity import FlashbirdOdometerEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
):

    _LOGGER.debug("Calling async_setup_entry entry=%s", entry)

    async_add_entities([
        FlashbirdRefreshEntity(hass, entry),
        FlashbirdOdometerEntity(hass, entry),
    ], True)