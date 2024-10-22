import logging

from homeassistant.core import HomeAssistant, callback, Event
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.const import UnitOfLength

from ..const import EVT_DEVICE_INFO_RETRIEVED
from ..helpers.device_info import define_device_info

_LOGGER = logging.getLogger(__name__)


class FlashbirdConnectedEntity(BinarySensorEntity):
    _hass: HomeAssistant
    _config: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        configEntry: ConfigEntry,
    ) -> None:

        self._hass = hass
        self._config = configEntry

        self._attr_has_entity_name = True
        self._attr_unique_id = self._config.entry_id + '_is_connected'
        self._attr_translation_key = 'is_connected'

    @property
    def should_poll(self) -> bool:
        return False

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
    async def async_added_to_hass(self):
        cancel = self._hass.bus.async_listen(
            EVT_DEVICE_INFO_RETRIEVED, self._refresh)
        self.async_on_remove(cancel)

    @callback
    async def _refresh(self, event: Event):
        _LOGGER.debug('refresh')

        isLocked = event.data['status']['isConnectedToGSM']
        if (self.is_on != isLocked):
            self._attr_is_on = isLocked
            self.async_write_ha_state()
