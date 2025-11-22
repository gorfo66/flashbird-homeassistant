"""Abstract base class for Flashbird sensor entities."""

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.flashbird.data import FlashbirdConfigEntry
from custom_components.flashbird.helpers.device_info import define_device_info
from custom_components.flashbird.helpers.flashbird_device_info import (
    FlashbirdDeviceInfo,
)


class AbstractFlashbirdSensorEntity(CoordinatorEntity, SensorEntity):
    """References the total mileage, e.g., the odometer."""

    _hass: HomeAssistant
    _config: ConfigEntry
    _logger = logging.getLogger(__name__)
    _update_if_none = False

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: FlashbirdConfigEntry,
    ) -> None:
        """Create the entity."""
        super().__init__(config_entry.runtime_data.coordinator)
        self._hass = hass
        self._config = config_entry
        self._attr_has_entity_name = True

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for the entity."""
        return define_device_info(self._config)

    def _get_flashbird_device_info(self) -> FlashbirdDeviceInfo:
        """Return the flashbird device information from the coordinator."""
        device_info: FlashbirdDeviceInfo = self.coordinator.data
        return device_info

    def _get_updated_data(self) -> None:
        """Return the data using the device info."""
        msg = "Please Implement this method."
        raise NotImplementedError(msg)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._logger.debug("refresh")
        new_value = self._get_updated_data()
        if (new_value is not None or self._update_if_none) and (
            self.native_value != new_value
        ):
            self._attr_native_value = new_value
            self.async_write_ha_state()
