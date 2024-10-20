import logging
from datetime import timedelta, datetime, timezone

from homeassistant.core import HomeAssistant, callback, Event
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.const import EntityCategory

from ..const import REFRESH_RATE, CONF_TOKEN, CONF_TRACKER_ID, EVT_DEVICE_INFO_RETRIEVED, EVT_NEED_REFRESH
from ..helpers.flashbird_api import flashbird_get_device_info
from ..helpers.device_info import define_device_info

_LOGGER = logging.getLogger(__name__)


class FlashbirdRefreshEntity(SensorEntity):
    """La classe de l'entité TutoHacs qui écoute la première"""

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
        self._attr_unique_id = self._config.entry_id + '_last_refresh'
        self._attr_translation_key = 'last_refresh'
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def icon(self) -> str | None:
        return "mdi:timer-settings-outline"

    @property
    def device_class(self) -> SensorDeviceClass | None:
        return SensorDeviceClass.TIMESTAMP

    @property
    def device_info(self) -> DeviceInfo:
        return define_device_info(self._config)

    @callback
    async def async_added_to_hass(self):
        
        cancelTimer = async_track_time_interval(
            self._hass,
            self._refresh,
            interval=timedelta(seconds=REFRESH_RATE),
        )

        cancelEventBus = self._hass.bus.async_listen(
            EVT_NEED_REFRESH, self._refresh)
        
        self.async_on_remove(cancelTimer)       
        self.async_on_remove(cancelEventBus)

    @callback
    async def _refresh(self, event: Event):
        _LOGGER.debug('Refresh sensors from Api call')
        
        deviceInfo = await self._hass.async_add_executor_job(flashbird_get_device_info, self._config.data[CONF_TOKEN], self._config.data[CONF_TRACKER_ID])
        self._hass.bus.fire(EVT_DEVICE_INFO_RETRIEVED, deviceInfo)
        self._attr_native_value = datetime.now(timezone.utc)

        # On sauvegarde le nouvel état
        self.async_write_ha_state()