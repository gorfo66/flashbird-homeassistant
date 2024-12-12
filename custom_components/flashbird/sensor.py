import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entities.flashbird_mileage_entity import FlashbirdMileageEntity
from .entities.flashbird_battery_entity import FlashbirdBatteryEntity
from .entities.flashbird_bike_battery_entity import FlashbirdBikeBatteryEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Do the setup all the sensor entities."""
    _LOGGER.debug("Calling async_setup_entry entry=%s", entry.entry_id)

    async_add_entities(
        [
            FlashbirdMileageEntity(hass, entry),
            FlashbirdBatteryEntity(hass, entry),
            FlashbirdBikeBatteryEntity(hass, entry),
        ],
        update_before_add=False,
    )
