import logging
from datetime import UTC, datetime, timedelta

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.event import async_track_time_interval

from ..const import (
    CONF_TOKEN,
    CONF_TRACKER_ID,
    EVT_DEVICE_INFO_RETRIEVED,
    EVT_NEED_REFRESH,
    REFRESH_RATE,
)
from ..helpers.device_info import define_device_info
from ..helpers.flashbird_api import flashbird_get_device_info
from ..coordinator import FlashbirdDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class FlashbirdRefreshEntity(SensorEntity):
    """Technical entity that periodically calls the API and displays the last refresh timestamp online"""

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
        self._attr_unique_id = self._config.entry_id + "_last_refresh"
        self._attr_translation_key = "last_refresh"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def icon(self) -> str | None:
        return "mdi:refresh"

    @property
    def device_class(self) -> SensorDeviceClass | None:
        return SensorDeviceClass.TIMESTAMP

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

        self._attr_native_value = datetime.now(UTC)

        # On sauvegarde le nouvel état
        self.async_write_ha_state()
