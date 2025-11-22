"""Entity for the smart key battery level."""

import logging

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo

from custom_components.flashbird.data import FlashbirdConfigEntry
from custom_components.flashbird.entities.abstract_flashbird_sensor_entity import (
    AbstractFlashbirdSensorEntity,
)
from custom_components.flashbird.helpers.device_info import define_device_info_key


class FlashbirdKeyBatteryEntity(AbstractFlashbirdSensorEntity):
    """References the battery of the smart key."""

    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: FlashbirdConfigEntry,
    ) -> None:
        """Create the key battery entity."""
        super().__init__(hass, config_entry)
        self._attr_unique_id = self._config.entry_id + "_key_battery"
        self._attr_translation_key = "key_battery"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def icon(self) -> str | None:
        """Return the icon for the entity."""
        return "mdi:battery-outline"

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the device class."""
        return SensorDeviceClass.BATTERY

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the native unit of measurement."""
        return "%"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for the smart key."""
        return define_device_info_key(self._config)

    def _get_updated_data(self) -> int:
        """Return the battery value from the first smart key."""
        return self._get_flashbird_device_info().get_first_smartkey_battery()
