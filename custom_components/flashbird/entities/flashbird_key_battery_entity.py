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

from ..data import FlashbirdConfigEntry
from ..helpers.flashbird_device_info import FlashbirdDeviceInfo
from ..helpers.device_info import define_device_info_key

_LOGGER = logging.getLogger(__name__)


class FlashbirdKeyBatteryEntity(CoordinatorEntity, SensorEntity):
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
        self._attr_unique_id = self._config.entry_id + "_key_battery"
        self._attr_translation_key = "key_battery"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def icon(self) -> str | None:
        return "mdi:battery-outline"

    @property
    def device_class(self) -> SensorDeviceClass | None:
        return SensorDeviceClass.BATTERY

    @property
    def native_unit_of_measurement(self) -> str | None:
        return "%"

    @property
    def device_info(self) -> DeviceInfo:
        return define_device_info_key(self._config)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("refresh")

        device_info: FlashbirdDeviceInfo = self.coordinator.data
        new_value = device_info.get_first_smartkey_battery()
        if new_value is not None:
            if self.native_value != new_value:
                self._attr_native_value = new_value
                self.async_write_ha_state()
