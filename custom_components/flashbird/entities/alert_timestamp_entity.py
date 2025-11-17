"""Entity for the current alert timestamp."""

import logging

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant

from custom_components.flashbird.data import FlashbirdConfigEntry
from custom_components.flashbird.entities.abstract_flashbird_sensor_entity import (
    AbstractFlashbirdSensorEntity,
)


class FlashbirdAlertTimestampEntity(AbstractFlashbirdSensorEntity):
    """The alert timestamp."""

    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: FlashbirdConfigEntry,
    ) -> None:
        """Create the alert timestamp entity."""
        super().__init__(hass, config_entry)
        self._attr_unique_id = self._config.entry_id + "_alert_timestamp"
        self._attr_translation_key = "alert_timestamp"

    @property
    def icon(self) -> str | None:
        """Return the icon for the entity."""
        return "mdi:alert"

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the device class."""
        return SensorDeviceClass.TIMESTAMP

    def _get_updated_data(self) -> str | None:
        """Return the current alert timestamp from the device info."""
        return self._get_flashbird_device_info().get_current_alert_timestamp()
