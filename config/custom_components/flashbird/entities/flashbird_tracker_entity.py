import logging

from homeassistant.core import HomeAssistant, callback, Event
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.device_tracker import TrackerEntity
from homeassistant.helpers.entity import DeviceInfo
from ..const import EVT_DEVICE_INFO_RETRIEVED
from ..helpers.device_info import define_device_info
_LOGGER = logging.getLogger(__name__)


class FlashbirdTrackerEntity(TrackerEntity):

    _hass: HomeAssistant
    _config: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,  # pylint: disable=unused-argument
        configEntry: ConfigEntry,  # pylint: disable=unused-argument
    ) -> None:
        
        self._hass = hass
        self._config = configEntry

        self._attr_has_entity_name = True
        self._attr_unique_id = self._config.entry_id + '_tracker'
        self._attr_translation_key = 'tracker'
        self._attr_entity_category = None
        self._attr_location_accuracy = 1        

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def icon(self) -> str | None:
        return "mdi:map-marker"

    @property
    def device_info(self) -> DeviceInfo:
        return define_device_info(self._config)

    @callback
    async def async_added_to_hass(self):
        cancel = self._hass.bus.async_listen(EVT_DEVICE_INFO_RETRIEVED, self._refresh)        
        self.async_on_remove(cancel)

    @callback
    async def _refresh(self, event: Event):
        _LOGGER.debug('refresh')

        longitude = event.data['longitude']
        latitude = event.data['latitude']

        if (longitude != self.longitude or latitude != self.latitude):
          self._attr_longitude = longitude
          self._attr_latitude = latitude
          self.async_write_ha_state()