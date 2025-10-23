import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entities.flashbird_mileage_entity import FlashbirdMileageEntity
from .entities.flashbird_battery_entity import FlashbirdBatteryEntity
from .entities.flashbird_bike_battery_entity import FlashbirdBikeBatteryEntity
from .entities.flashbird_key_battery_entity import FlashbirdKeyBatteryEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Do the setup all the sensor entities."""
    _LOGGER.debug("Calling async_setup_entry entry=%s", entry.entry_id)

    coordinator = entry.runtime_data.coordinator
    
    entries = [
      FlashbirdMileageEntity(hass, entry),
      FlashbirdBatteryEntity(hass, entry),
      FlashbirdBikeBatteryEntity(hass, entry)
    ]

    # Check if we have data for the smart key before to add it for creation
    smartKeys = coordinator.data.get('smartKeys', []) if coordinator.data else []
    if smartKeys:
      entries.append(FlashbirdKeyBatteryEntity(hass, entry))
    else:
      _LOGGER.debug('No smart key found')

    # Create the entities
    async_add_entities(entries, update_before_add=False)
