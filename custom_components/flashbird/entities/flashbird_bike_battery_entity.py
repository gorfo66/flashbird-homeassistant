"""Entity for the bike battery level in volt."""

import logging

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfElectricPotential
from homeassistant.core import HomeAssistant

from custom_components.flashbird.data import FlashbirdConfigEntry
from custom_components.flashbird.entities.abstract_flashbird_sensor_entity import (
    AbstractFlashbirdSensorEntity,
)


class FlashbirdBikeBatteryEntity(AbstractFlashbirdSensorEntity):
    """References the bike battery level in volt."""

    _logger = logging.getLogger(__name__)

    def __init__(self, hass: HomeAssistant, config_entry: FlashbirdConfigEntry) -> None:
        """Create the bike battery entity."""
        super().__init__(hass, config_entry)
        self._attr_unique_id = self._config.entry_id + "_bike_battery"
        self._attr_translation_key = "bike_battery"

    @property
    def icon(self) -> str | None:
        """Return the icon for the entity."""
        return "mdi:car-battery"

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the device class."""
        return SensorDeviceClass.VOLTAGE

    @property
    def state_class(self) -> SensorStateClass | None:
        """Return the state class."""
        return SensorStateClass.MEASUREMENT

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the native unit of measurement."""
        return UnitOfElectricPotential.VOLT

    def _get_updated_data(self) -> float:
        """Return the updated data."""
        data = self._get_flashbird_device_info().get_motorcycle_battery_voltage()
        if data is not None:
            return round(data / 1000, 2)
        return None
