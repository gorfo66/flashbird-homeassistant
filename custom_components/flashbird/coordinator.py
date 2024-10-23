"""DataUpdateCoordinator for integration_blueprint."""

import logging

from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant,Event
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, REFRESH_RATE, EVT_NEED_REFRESH, EVT_DEVICE_INFO_RETRIEVED, CONF_TOKEN, CONF_TRACKER_ID
    
from .helpers.flashbird_api import flashbird_get_device_info
from .data import FlashbirdConfigEntry

_LOGGER = logging.getLogger(__name__)


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class FlashbirdDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: FlashbirdConfigEntry

    def __init__(
        self,
        hass: HomeAssistant
    ) -> None:
        """Initialize."""

        _LOGGER.debug('create coordinator')

        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=REFRESH_RATE),
            always_update=True, 
        )

        # the trigger the refresh in case there is a manual need to refresh the data
        self.hass.bus.async_listen(EVT_NEED_REFRESH, self._fetch_data)
    

    async def _async_update_data(self) -> None:
        """Update data via library."""

        _LOGGER.debug('asynchronous update')
        await self._fetch_data(event=None)
    
    async def _fetch_data(self, event: Event) -> None:
        """Fetch data from the API."""


        _LOGGER.debug('fetch data')
        deviceInfo = await self.hass.async_add_executor_job(
            flashbird_get_device_info,
            self.config_entry.data[CONF_TOKEN],
            self.config_entry.data[CONF_TRACKER_ID],
        )
        self.hass.bus.fire(EVT_DEVICE_INFO_RETRIEVED, deviceInfo)