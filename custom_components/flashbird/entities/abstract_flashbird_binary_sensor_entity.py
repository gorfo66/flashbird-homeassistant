"""Abstract base class for Flashbird binary sensor entities."""

import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.flashbird.data import FlashbirdConfigEntry
from custom_components.flashbird.helpers.device_info import define_device_info
from custom_components.flashbird.helpers.flashbird_device_info import (
    FlashbirdDeviceInfo,
)


class AbstractFlashbirdBinarySensorEntity(CoordinatorEntity, BinarySensorEntity):
    """References the total mileage, e.g., the odometer."""

    _hass: HomeAssistant
    _config: ConfigEntry
    _logger = logging.getLogger(__name__)

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

    def _get_updated_data(self) -> bool:
        """Return the data using the device info."""
        msg = "Please Implement this method."
        raise NotImplementedError(msg)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._logger.debug("refresh")
        is_connected = self._get_updated_data()
        if is_connected is not None and self.is_on != is_connected:
            self._attr_is_on = is_connected
            self.async_write_ha_state()
