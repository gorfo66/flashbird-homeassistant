import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfLength
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..data import FlashbirdConfigEntry
from ..helpers.flashbird_device_info import FlashbirdDeviceInfo
from ..helpers.device_info import define_device_info

_LOGGER = logging.getLogger(__name__)


class FlashbirdMileageEntity(CoordinatorEntity, SensorEntity):
    """References the total mileage e.g. the mileage"""

    _hass: HomeAssistant
    _config: ConfigEntry

    def __init__(self, hass: HomeAssistant, configEntry: FlashbirdConfigEntry) -> None:
        super().__init__(configEntry.runtime_data.coordinator)

        self._hass = hass
        self._config = configEntry

        self._attr_has_entity_name = True
        self._attr_unique_id = self._config.entry_id + "_mileage"
        self._attr_translation_key = "mileage"

    @property
    def icon(self) -> str | None:
        return "mdi:counter"

    @property
    def device_class(self) -> SensorDeviceClass | None:
        return SensorDeviceClass.DISTANCE

    @property
    def state_class(self) -> SensorStateClass | None:
        return SensorStateClass.TOTAL_INCREASING

    @property
    def native_unit_of_measurement(self) -> str | None:
        return UnitOfLength.KILOMETERS

    @property
    def device_info(self) -> DeviceInfo:
        return define_device_info(self._config)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("refresh")
        device_info: FlashbirdDeviceInfo = self.coordinator.data
        totalDistance = device_info.get_total_distance()
        if totalDistance is not None:
            distance = round(totalDistance / 1000)
            if self.native_value != distance:
                self._attr_native_value = distance
                self.async_write_ha_state()
