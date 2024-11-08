import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfLength
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..helpers.device_info import define_device_info
from ..data import FlashbirdConfigEntry

_LOGGER = logging.getLogger(__name__)


class FlashbirdConnectedEntity(CoordinatorEntity, BinarySensorEntity):
    """Entity that references the GSM network connectivity"""

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
        self._attr_unique_id = self._config.entry_id + "_is_connected"
        self._attr_translation_key = "is_connected"

    @property
    def icon(self) -> str | None:
        return "mdi:wifi"

    @property
    def device_class(self) -> BinarySensorDeviceClass | None:
        return BinarySensorDeviceClass.CONNECTIVITY

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
        isConnected = self.coordinator.data["status"]["isConnectedToGSM"]
        if self.is_on != isConnected:
            self._attr_is_on = isConnected
            self.async_write_ha_state()
