"""Instantiate sensor entities."""

import logging
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.flashbird.entities.flashbird_battery_entity import (
    FlashbirdBatteryEntity,
)
from custom_components.flashbird.entities.flashbird_bike_battery_entity import (
    FlashbirdBikeBatteryEntity,
)
from custom_components.flashbird.entities.flashbird_key_battery_entity import (
    FlashbirdKeyBatteryEntity,
)
from custom_components.flashbird.entities.flashbird_last_refresh_entity import (
    FlashbirdLastRefreshEntity,
)
from custom_components.flashbird.entities.flashbird_mileage_entity import (
    FlashbirdMileageEntity,
)

if TYPE_CHECKING:
    from .helpers.flashbird_device_info import FlashbirdDeviceInfo


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Do the setup all the sensor entities."""
    _LOGGER.debug("Calling async_setup_entry entry=%s", entry.entry_id)

    device_info: FlashbirdDeviceInfo = entry.runtime_data.coordinator.data

    entries = []

    # Mileage is always present
    entries.append(FlashbirdMileageEntity(hass, entry))
    entries.append(FlashbirdLastRefreshEntity(hass, entry))

    # Check if we have data for the smart key before to add it for creation
    if device_info.get_smart_keys():
        entries.append(FlashbirdKeyBatteryEntity(hass, entry))
    else:
        _LOGGER.debug("No smart key found")

    # Check if we have motorbike battery voltage before to add the sensor
    if device_info.get_motorcycle_battery_voltage():
        entries.append(FlashbirdBikeBatteryEntity(hass, entry))
    else:
        _LOGGER.debug("No motorbike battery voltage found")

    # Check if we have tracker battery percentage before to add the sensor
    if device_info.get_battery_percentage():
        entries.append(FlashbirdBatteryEntity(hass, entry))
    else:
        _LOGGER.debug("No tracker battery information found")

    # Create the entities
    async_add_entities(entries, update_before_add=False)
