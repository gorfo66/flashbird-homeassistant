"""Entity for the total mileage."""

import logging

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfLength
from homeassistant.core import HomeAssistant

from custom_components.flashbird.data import FlashbirdConfigEntry
from custom_components.flashbird.entities.abstract_flashbird_sensor_entity import (
    AbstractFlashbirdSensorEntity,
)


class FlashbirdMileageEntity(AbstractFlashbirdSensorEntity):
    """References the total mileage, e.g., the mileage."""

    _logger = logging.getLogger(__name__)

    def __init__(self, hass: HomeAssistant, config_entry: FlashbirdConfigEntry) -> None:
        """Create the mileage entity."""
        super().__init__(hass, config_entry)
        self._attr_unique_id = self._config.entry_id + "_mileage"
        self._attr_translation_key = "mileage"

    @property
    def icon(self) -> str | None:
        """Return the icon for the entity."""
        return "mdi:counter"

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the device class."""
        return SensorDeviceClass.DISTANCE

    @property
    def state_class(self) -> SensorStateClass | None:
        """Return the state class."""
        return SensorStateClass.TOTAL_INCREASING

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the native unit of measurement."""
        return UnitOfLength.KILOMETERS
    
    @property
    def suggested_display_precision(self) -> int:
        """Return the suggested precision."""
        return 0

    def _get_updated_data(self) -> int:
        """Return the total mileage in kilometers from the device info."""
        total_distance = self._get_flashbird_device_info().get_total_distance()
        if total_distance is not None:
            return round(total_distance / 1000)
        return None
