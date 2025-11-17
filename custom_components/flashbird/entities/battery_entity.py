"""Entity for the tracker battery level."""

import logging

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant

from custom_components.flashbird.data import FlashbirdConfigEntry
from custom_components.flashbird.entities.abstract_flashbird_sensor_entity import (
    AbstractFlashbirdSensorEntity,
)


class FlashbirdBatteryEntity(AbstractFlashbirdSensorEntity):
    """References the tracker battery level."""

    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: FlashbirdConfigEntry,
    ) -> None:
        """Create the battery entity."""
        super().__init__(hass, config_entry)
        self._attr_unique_id = self._config.entry_id + "_battery"
        self._attr_translation_key = "battery"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def icon(self) -> str | None:
        """Return the icon for the entity."""
        return "mdi:battery-outline"

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the device class."""
        return SensorDeviceClass.BATTERY

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the native unit of measurement."""
        return "%"

    def _get_updated_data(self) -> int:
        """Return the updated data."""
        return self._get_flashbird_device_info().get_battery_percentage()
