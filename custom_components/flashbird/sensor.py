import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entities.flashbird_odometer_entity import FlashbirdOdometerEntity
from .entities.flashbird_refresh_entity import FlashbirdRefreshEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Do the setup all the sensor entities."""
    _LOGGER.debug("Calling async_setup_entry entry=%s", entry)

    coordinator = entry.runtime_data.coordinator

    async_add_entities(
        [
            FlashbirdRefreshEntity(hass, entry, coordinator),
            FlashbirdOdometerEntity(hass, entry, coordinator),
        ],
        update_before_add=True,
    )
