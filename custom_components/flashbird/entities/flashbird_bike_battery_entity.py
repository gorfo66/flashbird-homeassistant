import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfElectricPotential
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..data import FlashbirdConfigEntry
from ..helpers.flashbird_device_info import FlashbirdDeviceInfo
from ..helpers.device_info import define_device_info

_LOGGER = logging.getLogger(__name__)


class FlashbirdBikeBatteryEntity(CoordinatorEntity, SensorEntity):
    """References the total mileage e.g. the mileage"""

    _hass: HomeAssistant
    _config: ConfigEntry

    def __init__(self, hass: HomeAssistant, configEntry: FlashbirdConfigEntry) -> None:
        super().__init__(configEntry.runtime_data.coordinator)

        self._hass = hass
        self._config = configEntry

        self._attr_has_entity_name = True
        self._attr_unique_id = self._config.entry_id + "_bike_battery"
        self._attr_translation_key = "bike_battery"

    @property
    def icon(self) -> str | None:
        return "mdi:car-battery"

    @property
    def device_class(self) -> SensorDeviceClass | None:
        return SensorDeviceClass.VOLTAGE

    @property
    def state_class(self) -> SensorStateClass | None:
        return SensorStateClass.MEASUREMENT

    @property
    def native_unit_of_measurement(self) -> str | None:
        return UnitOfElectricPotential.VOLT

    @property
    def device_info(self) -> DeviceInfo:
        return define_device_info(self._config)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("refresh")
        device_info: FlashbirdDeviceInfo = self.coordinator.data
        voltageInMillivolt = device_info.get_motorcycle_battery_voltage()
        if voltageInMillivolt is not None:
            new_value = round(voltageInMillivolt / 1000, 2)
            if self.native_value != new_value:
                self._attr_native_value = new_value
                self.async_write_ha_state()
