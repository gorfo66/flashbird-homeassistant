import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..helpers.device_info import define_device_info
from ..data import FlashbirdConfigEntry

_LOGGER = logging.getLogger(__name__)


class FlashbirdBatteryEntity(CoordinatorEntity, SensorEntity):
    """References the total mileage e.g. the odometer"""

    _hass: HomeAssistant
    _config: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        configEntry: FlashbirdConfigEntry,
    ) -> None:

        super().__init__(configEntry.runtime_data.coordinator)

        self._hass = hass
        self._config = configEntry

        self._attr_has_entity_name = True
        self._attr_unique_id = self._config.entry_id + "_battery"
        self._attr_translation_key = "battery"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def icon(self) -> str | None:
        return "mdi:battery-outline"

    @property
    def device_class(self) -> SensorDeviceClass | None:
        return SensorDeviceClass.BATTERY

    @property
    def native_unit_of_measurement(self) -> str | None:
        return '%'

    @property
    def device_info(self) -> DeviceInfo:
        return define_device_info(self._config)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug('refresh')
        newValue = self.coordinator.data['batteryPercentage']
        if self.native_value != newValue:
            self._attr_native_value = newValue
            self.async_write_ha_state()
