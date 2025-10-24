import logging

from homeassistant.components.device_tracker import TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..data import FlashbirdConfigEntry
from ..helpers.flashbird_device_info import FlashbirdDeviceInfo
from ..helpers.device_info import define_device_info

_LOGGER = logging.getLogger(__name__)


class FlashbirdTrackerEntity(CoordinatorEntity, TrackerEntity):
    """Refers to the tracker position"""

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
        self._attr_unique_id = self._config.entry_id + "_tracker"
        self._attr_translation_key = "tracker"
        self._attr_entity_category = None
        self._attr_location_accuracy = 1

    @property
    def icon(self) -> str | None:
        return "mdi:map-marker"

    @property
    def device_info(self) -> DeviceInfo:
        return define_device_info(self._config)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("refresh")
        device_info: FlashbirdDeviceInfo = self.coordinator.data
        longitude = device_info.get_longitude()
        latitude = device_info.get_latitude()

        if longitude is not None and latitude is not None:
            if longitude != self.longitude or latitude != self.latitude:
                self._attr_longitude = longitude
                self._attr_latitude = latitude
                self.async_write_ha_state()
