"""Entity for GSM network connectivity."""

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
)
from homeassistant.const import UnitOfLength
from homeassistant.core import HomeAssistant

from custom_components.flashbird.data import FlashbirdConfigEntry
from custom_components.flashbird.entities.abstract_flashbird_binary_sensor_entity import (
    AbstractFlashbirdBinarySensorEntity,
)


class FlashbirdConnectedEntity(AbstractFlashbirdBinarySensorEntity):
    """Entity that references the GSM network connectivity."""

    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: FlashbirdConfigEntry,
    ) -> None:
        """Create the connected entity."""
        super().__init__(hass, config_entry)
        self._attr_unique_id = self._config.entry_id + "_is_connected"
        self._attr_translation_key = "is_connected"

    @property
    def icon(self) -> str | None:
        """Return the icon for the entity."""
        return "mdi:wifi"

    @property
    def device_class(self) -> BinarySensorDeviceClass | None:
        """Return the device class."""
        return BinarySensorDeviceClass.CONNECTIVITY

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the native unit of measurement."""
        return UnitOfLength.KILOMETERS

    def _get_updated_data(self) -> float:
        """Return the updated data."""
        return self._get_flashbird_device_info().is_connected_to_gsm()
