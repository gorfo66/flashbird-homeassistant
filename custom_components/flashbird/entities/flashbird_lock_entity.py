"""Entity for the alert lock, allowing lock/unlock and status display."""

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.lock import LockEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.flashbird.const import CONF_TOKEN, CONF_TRACKER_ID
from custom_components.flashbird.data import FlashbirdConfigEntry
from custom_components.flashbird.helpers.device_info import define_device_info
from custom_components.flashbird.helpers.flashbird_api import flashbird_set_lock_enabled

if TYPE_CHECKING:
    from custom_components.flashbird.helpers.flashbird_device_info import (
        FlashbirdDeviceInfo,
    )


class FlashbirdLockEntity(CoordinatorEntity, LockEntity):
    """References the alert lock. Allows to lock/unlock the alerts and display the status."""

    _hass: HomeAssistant
    _config: ConfigEntry
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: FlashbirdConfigEntry,
    ) -> None:
        """Create the class."""
        super().__init__(config_entry.runtime_data.coordinator)

        self._hass = hass
        self._config = config_entry

        self._attr_has_entity_name = True
        self._attr_unique_id = self._config.entry_id + "_lock"
        self._attr_entity_category = None
        self._attr_location_accuracy = 1

        self._attr_translation_key = "lock"

    @property
    def icon(self) -> str | None:
        """Return the icon for the entity."""
        return "mdi:shield-lock-outline"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for the entity."""
        return define_device_info(self._config)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._logger.debug("refresh")
        device_info: FlashbirdDeviceInfo = self.coordinator.data
        is_locked = device_info.is_lock_enabled()
        if is_locked is not None and self.is_locked != is_locked:
            self._attr_is_locked = is_locked
            self._attr_is_locking = False
            self._attr_is_unlocking = False
            self.async_write_ha_state()

    async def async_lock(self, **kwargs: Any) -> None:
        """Lock the entity."""
        _ = kwargs
        self._logger.debug("lock")
        self._attr_is_locking = True
        self.async_write_ha_state()
        await self._hass.async_add_executor_job(
            flashbird_set_lock_enabled,
            self._config.data[CONF_TOKEN],
            self._config.data[CONF_TRACKER_ID],
            True,
        )

    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock the entity."""
        _ = kwargs
        self._logger.debug("unlock")
        self._attr_is_unlocking = True
        self.async_write_ha_state()
        await self._hass.async_add_executor_job(
            flashbird_set_lock_enabled,
            self._config.data[CONF_TOKEN],
            self._config.data[CONF_TRACKER_ID],
            False,
        )
