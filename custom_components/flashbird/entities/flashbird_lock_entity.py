import logging

from homeassistant.components.lock import LockEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import CONF_TOKEN, CONF_TRACKER_ID
from ..helpers.device_info import define_device_info
from ..helpers.flashbird_api import flashbird_set_lock_enabled
from ..data import FlashbirdConfigEntry

_LOGGER = logging.getLogger(__name__)


class FlashbirdLockEntity(CoordinatorEntity, LockEntity):
    """References the alert lock. Allows to lock/unlock the alerts and display the status"""

    _hass: HomeAssistant
    _config: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        configEntry: FlashbirdConfigEntry,
    ) -> None:

        super().__init__(configEntry.runtime_data.coordinator)

        self._hass = hass
        self._config = configEntry

        self._attr_has_entity_name = True
        self._attr_unique_id = self._config.entry_id + "_lock"
        self._attr_entity_category = None
        self._attr_location_accuracy = 1

        self._attr_translation_key = "lock"

    @property
    def icon(self) -> str | None:
        return "mdi:shield-lock-outline"

    @property
    def device_info(self) -> DeviceInfo:
        return define_device_info(self._config)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("refresh")
        isLocked = self.coordinator.data["lockEnabled"]
        if self.is_locked != isLocked:
            self._attr_is_locked = isLocked
            self._attr_is_locking = False
            self._attr_is_unlocking = False
            self.async_write_ha_state()

    async def async_lock(self, **kwargs):
        _LOGGER.debug("lock")
        self._attr_is_locking = True
        self.async_write_ha_state()
        await self._hass.async_add_executor_job(
            flashbird_set_lock_enabled,
            self._config.data[CONF_TOKEN],
            self._config.data[CONF_TRACKER_ID],
            True
        )
        await self.coordinator.async_request_refresh()

    async def async_unlock(self, **kwargs):
        _LOGGER.debug("unlock")
        self._attr_is_unlocking = True
        self.async_write_ha_state()
        await self._hass.async_add_executor_job(
            flashbird_set_lock_enabled,
            self._config.data[CONF_TOKEN],
            self._config.data[CONF_TRACKER_ID],
            False
        )
        await self.coordinator.async_request_refresh()
