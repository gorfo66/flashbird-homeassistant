"""DataUpdateCoordinator for integration_blueprint."""

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import *
from .helpers.flashbird_api import flashbird_get_device_info
from .helpers.flashbird_ws import flashbird_ws_register
from .helpers.flashbird_device_info import FlashbirdDeviceInfo

_LOGGER = logging.getLogger(__name__)


class FlashbirdDataUpdateCoordinator(DataUpdateCoordinator):

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize."""
        _LOGGER.debug("init")

        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=REFRESH_RATE),
            always_update=True,
        )    

        flashbird_ws_register(
            self.hass,
            self.config_entry.data[CONF_TOKEN],
            self.config_entry.data[CONF_TRACKER_ID],
            self.websocket_callback
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
        

    async def websocket_callback(self, device_info: FlashbirdDeviceInfo) -> None:
        """
        Callback method that the ws client is calling for each event
        """
        _LOGGER.debug("websocket callback")
        await self._preprocess_data(device_info)
        self.async_set_updated_data(device_info)


    async def refresh_data(self) -> None:
        _LOGGER.debug("refresh data")
        device_info = await self._fetch_data_from_api()
        self.async_set_updated_data(device_info)


    async def _fetch_data_from_api(self) -> FlashbirdDeviceInfo:
        _LOGGER.debug("fetch data from api")
        device_info = await self.hass.async_add_executor_job(
            flashbird_get_device_info,
            self.config_entry.data[CONF_TOKEN],
            self.config_entry.data[CONF_TRACKER_ID],
        )

        await self._preprocess_data(device_info)
        return device_info

    async def _preprocess_data(self, device_info: FlashbirdDeviceInfo) -> None:
        """
        Process the data before broadcasting it to the devices
        """
        _LOGGER.debug("preprocess data")
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


    async def _async_update_data(self) -> None:
        """
        Update data via library (periodic timer)
        """
        _LOGGER.debug("async update data")
        try:
            device_info = await self._fetch_data_from_api()
            return device_info
        except ValueError as err:
            raise ConfigEntryAuthFailed from err
