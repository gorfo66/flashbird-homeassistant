import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfLength
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo

from ..const import EVT_DEVICE_INFO_RETRIEVED
from ..helpers.device_info import define_device_info
from ..coordinator import FlashbirdDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class FlashbirdMileageEntity(SensorEntity):
    """References the total mileage e.g. the mileage"""

    _hass: HomeAssistant
    _config: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        configEntry: ConfigEntry,
        coordinator: FlashbirdDataUpdateCoordinator
    ) -> None:
        
        super().__init__(coordinator)
        
        self._hass = hass
        self._config = configEntry

        self._attr_has_entity_name = True
        self._attr_unique_id = self._config.entry_id + "_mileage"
        self._attr_translation_key = "mileage"

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def icon(self) -> str | None:
        return "mdi:counter"

    @property
    def device_class(self) -> SensorDeviceClass | None:
        return SensorDeviceClass.DISTANCE

    @property
    def state_class(self) -> SensorStateClass | None:
        return SensorStateClass.TOTAL_INCREASING

    @property
    def native_unit_of_measurement(self) -> str | None:
        return UnitOfLength.KILOMETERS

    @property
    def device_info(self) -> DeviceInfo:
        return define_device_info(self._config)

    @callback
    async def async_added_to_hass(self):
        cancel = self._hass.bus.async_listen(EVT_DEVICE_INFO_RETRIEVED, self._refresh)
        self.async_on_remove(cancel)

    @callback
    async def _refresh(self, event: Event):
        _LOGGER.debug("refresh")

        distance = event.data["statistics"]["totalDistance"] / 1000
        if self.native_value != distance:
            self._attr_native_value = distance
            self.async_write_ha_state()
