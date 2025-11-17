"""Entity for tracking websocket refresh rate."""

import logging

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import EntityCategory, UnitOfFrequency
from homeassistant.core import HomeAssistant

from custom_components.flashbird.data import FlashbirdConfigEntry
from custom_components.flashbird.entities.abstract_flashbird_sensor_entity import (
    AbstractFlashbirdSensorEntity,
)


class FlashbirdRefreshRateEntity(AbstractFlashbirdSensorEntity):
    """Entity that tracks the websocket refresh rate in Hz (updates per second)."""

    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: FlashbirdConfigEntry,
    ) -> None:
        """Create the refresh rate entity."""
        super().__init__(hass, config_entry)
        self._attr_unique_id = self._config.entry_id + "_refresh_rate"
        self._attr_translation_key = "refresh_rate"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def icon(self) -> str | None:
        """Return the icon for the entity."""
        return "mdi:update"

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the device class."""
        return SensorDeviceClass.FREQUENCY

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the native unit of measurement."""
        return UnitOfFrequency.HERTZ

    @property
    def suggested_display_precision(self) -> int:
        """Return the suggested precision."""
        return 5

    def _get_updated_data(self) -> float:
        """Return the refresh rate in Hz (updates per second)."""
        device_info = self._get_flashbird_device_info()
        if device_info:
            refresh_rate = device_info.get_refresh_rate()
            if refresh_rate is not None:
                return round(refresh_rate, 4)
        return 0.0
