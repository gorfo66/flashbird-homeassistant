import logging
from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.flashbird.data import FlashbirdConfigEntry
from custom_components.flashbird.helpers.device_info import define_device_info

if TYPE_CHECKING:
    from custom_components.flashbird.helpers.flashbird_device_info import (
        FlashbirdDeviceInfo,
    )


_LOGGER = logging.getLogger(__name__)


class FlashbirdBatteryEntity(CoordinatorEntity, SensorEntity):
    """References the total mileage, e.g., the odometer."""

    _hass: HomeAssistant
    _config: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: FlashbirdConfigEntry,
    ) -> None:
        """Create the battery entity."""
        super().__init__(config_entry.runtime_data.coordinator)
        self._hass = hass
        self._config = config_entry

        self._attr_has_entity_name = True
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

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for the entity."""
        return define_device_info(self._config)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("refresh")
        device_info: FlashbirdDeviceInfo = self.coordinator.data
        new_value = device_info.get_battery_percentage()
        if new_value is not None:
            if self.native_value != new_value:
                self._attr_native_value = new_value
                self.async_write_ha_state()
