import logging

from homeassistant.core import HomeAssistant, callback, Event
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.lock import LockEntity
from homeassistant.helpers.entity import DeviceInfo
from ..const import EVT_DEVICE_INFO_RETRIEVED, CONF_TOKEN, CONF_TRACKER_ID, EVT_NEED_REFRESH
from ..helpers.device_info import define_device_info
from ..helpers.flashbird_api import flashbird_set_lock_enabled

_LOGGER = logging.getLogger(__name__)


class FlashbirdLockEntity(LockEntity):

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
        self._attr_unique_id = self._config.entry_id + '_lock'
        self._attr_entity_category = None
        self._attr_location_accuracy = 1

        self._attr_translation_key = 'lock'

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def icon(self) -> str | None:
        return "mdi:shield-lock-outline"

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

        isLocked = event.data['lockEnabled']
        if (self.is_locked != isLocked):
            self._attr_is_locked = isLocked
            self._attr_is_locking = False
            self._attr_is_unlocking = False
            self.async_write_ha_state()

    async def async_lock(self, **kwargs):
        _LOGGER.debug('lock')
        self._attr_is_locking = True
        self.async_write_ha_state()
        await self._hass.async_add_executor_job(flashbird_set_lock_enabled, self._config.data[CONF_TOKEN], self._config.data[CONF_TRACKER_ID], True, self._after_lock_update)

    async def async_unlock(self, **kwargs):
        _LOGGER.debug('unlock')
        self._attr_is_unlocking = True
        self.async_write_ha_state()
        await self._hass.async_add_executor_job(flashbird_set_lock_enabled, self._config.data[CONF_TOKEN], self._config.data[CONF_TRACKER_ID], False, self._after_lock_update)

    @callback
    def _after_lock_update(self):
        self._hass.bus.fire(EVT_NEED_REFRESH)
