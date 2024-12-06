"""DataUpdateCoordinator for integration_blueprint."""

import logging

from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed

from .const import DOMAIN, REFRESH_RATE, CONF_TOKEN, CONF_TRACKER_ID, CONF_FIRMWARE_VERSION

from .helpers.flashbird_api import flashbird_get_device_info

_LOGGER = logging.getLogger(__name__)


class FlashbirdDataUpdateCoordinator(DataUpdateCoordinator):

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

    async def _async_setup(self):
        """Set up the coordinator

        This is the place to set up your coordinator,
        or to load data, that only needs to be loaded once.

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        _LOGGER.debug('async setup')

    async def _async_update_data(self) -> None:
        """Update data via library."""

        _LOGGER.debug('asynchronous update')
        try:
          deviceInfo = await self.hass.async_add_executor_job(
              flashbird_get_device_info,
              self.config_entry.data[CONF_TOKEN],
              self.config_entry.data[CONF_TRACKER_ID]
          )

          # get the firmware version and store it in the config entry, for the device
          firmwareVersion = deviceInfo['softVersion']
          if (self.config_entry.data[CONF_FIRMWARE_VERSION] != firmwareVersion):
              newConfig = self.config_entry.data.copy()
              newConfig[CONF_FIRMWARE_VERSION] = firmwareVersion
              self.hass.config_entries.async_update_entry(self.config_entry, data=newConfig)

          return deviceInfo
        except ValueError as err:
            raise ConfigEntryAuthFailed from err
