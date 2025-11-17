"""Entity for the last refresh timestamp from API/WS."""

import logging

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant

from custom_components.flashbird.data import FlashbirdConfigEntry
from custom_components.flashbird.entities.abstract_flashbird_sensor_entity import (
    AbstractFlashbirdSensorEntity,
)


class FlashbirdLastRefreshEntity(AbstractFlashbirdSensorEntity):
    """The last refresh from API / WS timestamp."""

    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: FlashbirdConfigEntry,
    ) -> None:
        """Create the last refresh entity."""
        super().__init__(hass, config_entry)
        self._attr_unique_id = self._config.entry_id + "_last_refresh"
        self._attr_translation_key = "last_refresh"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def icon(self) -> str | None:
        """Return the icon for the entity."""
        return "mdi:update"

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the device class."""
        return SensorDeviceClass.TIMESTAMP

    def _get_updated_data(self) -> str:
        """Return the last refresh timestamp from the device info."""
        return self._get_flashbird_device_info().get_last_refresh()
