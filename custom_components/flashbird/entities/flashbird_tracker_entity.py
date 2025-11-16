"""Entity for the device tracker position."""

import logging
from typing import TYPE_CHECKING

from homeassistant.components.device_tracker import TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.flashbird.data import FlashbirdConfigEntry
from custom_components.flashbird.helpers.device_info import define_device_info

if TYPE_CHECKING:
    from custom_components.flashbird.helpers.flashbird_device_info import (
        FlashbirdDeviceInfo,
    )


class FlashbirdTrackerEntity(CoordinatorEntity, TrackerEntity):
    """Refers to the tracker position."""

    _hass: HomeAssistant
    _config: ConfigEntry
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: FlashbirdConfigEntry,
    ) -> None:
        """Create the tracker entity."""
        super().__init__(config_entry.runtime_data.coordinator)
        self._hass = hass
        self._config = config_entry

        self._attr_has_entity_name = True
        self._attr_unique_id = self._config.entry_id + "_tracker"
        self._attr_translation_key = "tracker"
        self._attr_entity_category = None
        self._attr_location_accuracy = 1

    @property
    def icon(self) -> str | None:
        """Return the icon for the entity."""
        return "mdi:map-marker"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for the entity."""
        return define_device_info(self._config)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._logger.debug("refresh")
        device_info: FlashbirdDeviceInfo = self.coordinator.data
        longitude = device_info.get_longitude()
        latitude = device_info.get_latitude()

        if (longitude is not None and latitude is not None) and (
            longitude != self.longitude or latitude != self.latitude
        ):
            self._attr_longitude = longitude
            self._attr_latitude = latitude
            self.async_write_ha_state()
