"""DataUpdateCoordinator for integration_blueprint."""

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import *
from .helpers.flashbird_api import flashbird_get_device_info

_LOGGER = logging.getLogger(__name__)


class FlashbirdDataUpdateCoordinator(DataUpdateCoordinator):

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize."""
        _LOGGER.debug("create coordinator")

        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=REFRESH_RATE),
            always_update=True,
        )

    async def _async_setup(self) -> None:
        """
        Set up the coordinator

        This is the place to set up your coordinator,
        or to load data, that only needs to be loaded once.

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        _LOGGER.debug("async setup")

    async def _async_update_data(self) -> None:
        """Update data via library."""
        _LOGGER.debug("asynchronous update")
        try:
            device_info = await self.hass.async_add_executor_job(
                flashbird_get_device_info,
                self.config_entry.data[CONF_TOKEN],
                self.config_entry.data[CONF_TRACKER_ID],
            )

            # get the firmware version and store it in the config entry, for the device
            # get the model of the tracker and store it in the config entry, for the device
            firmware_version = device_info.get_soft_version()
            model = device_info.get_device_type().capitalize()
            if self.config_entry.data[CONF_FIRMWARE_VERSION] != firmware_version or self.config_entry.data[CONF_MODEL] != model:
                newConfig = self.config_entry.data.copy()
                newConfig[CONF_FIRMWARE_VERSION] = firmware_version
                newConfig[CONF_MODEL] = model
                self.hass.config_entries.async_update_entry(
                    self.config_entry, data=newConfig
                )

            # Update the serial of the smart key
            smart_key_serial = device_info.get_first_smartkey_serial()
            if smart_key_serial is not None:
                if self.config_entry.data.get(CONF_SERIAL_NUMBER_KEY) != smart_key_serial:
                    newConfig = self.config_entry.data.copy()
                    newConfig[CONF_SERIAL_NUMBER_KEY] = smart_key_serial
                    self.hass.config_entries.async_update_entry(
                        self.config_entry, data=newConfig
                    )
            else:
                _LOGGER.debug("No smart keys found for this device.")

            return device_info
        except ValueError as err:
            raise ConfigEntryAuthFailed from err
