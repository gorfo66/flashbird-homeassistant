"""Entity for the alert level."""

import logging

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant

from custom_components.flashbird.data import FlashbirdConfigEntry
from custom_components.flashbird.entities.abstract_flashbird_sensor_entity import (
    AbstractFlashbirdSensorEntity,
)


class FlashbirdAlertLevelEntity(AbstractFlashbirdSensorEntity):
    """The alert level."""

    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: FlashbirdConfigEntry,
    ) -> None:
        """Create the alert level entity."""
        super().__init__(hass, config_entry)
        self._attr_unique_id = self._config.entry_id + "_alert_level"
        self._attr_translation_key = "alert_level"

    @property
    def icon(self) -> str | None:
        """Return the icon for the entity."""
        return "mdi:alert"

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the device class."""
        return SensorDeviceClass.ENUM

    @property
    def options(self) -> list[str]:
        """Return the list of available alert levels."""
        return [
            "no_alert",
            "shake_detected",
            "repeated_shake_detected",
            "movement_detected",
        ]

    def _get_updated_data(self) -> str:
        """Return the alert level."""
        device_info = self._get_flashbird_device_info()
        if device_info:
            alert_level = device_info.get_current_alert_level()
            if alert_level is not None:
                level_map = {
                    1: "shake_detected",
                    2: "repeated_shake_detected",
                    3: "movement_detected",
                }
                return level_map.get(alert_level, "no_alert")
        return "no_alert"
