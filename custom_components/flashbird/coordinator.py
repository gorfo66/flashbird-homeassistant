"""DataUpdateCoordinator for integration_blueprint."""

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.flashbird.const import (
    CONF_FIRMWARE_VERSION,
    CONF_MODEL,
    CONF_SERIAL_NUMBER_KEY,
    CONF_TOKEN,
    CONF_TRACKER_ID,
    DOMAIN,
    REFRESH_RATE,
)
from custom_components.flashbird.helpers.flashbird_api import flashbird_get_device_info
from custom_components.flashbird.helpers.flashbird_device_info import (
    FlashbirdDeviceInfo,
)
from custom_components.flashbird.helpers.flashbird_ws import flashbird_ws_register

_LOGGER = logging.getLogger(__name__)


class FlashbirdDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator for Flashbird data updates from the API and WebSocket."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the data update coordinator."""
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
            self.config_entry,
            self.websocket_callback,
        )

    async def _async_setup(self) -> None:
        """Set up the coordinator (called during first refresh)."""
        _LOGGER.debug("async setup")

    async def websocket_callback(self, device_info: FlashbirdDeviceInfo) -> None:
        """Handle websocket callback for each event."""
        _LOGGER.debug("websocket callback")
        self.async_set_updated_data(device_info)

    async def refresh_data(self) -> None:
        """Refresh data from the API and update coordinator."""
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
        """Process the data before broadcasting it to the devices."""
        _LOGGER.debug("preprocess data")
        firmware_version = device_info.get_soft_version()
        model = device_info.get_device_type().capitalize()
        if (
            self.config_entry.data[CONF_FIRMWARE_VERSION] != firmware_version
            or self.config_entry.data[CONF_MODEL] != model
        ):
            new_config = self.config_entry.data.copy()
            new_config[CONF_FIRMWARE_VERSION] = firmware_version
            new_config[CONF_MODEL] = model
            self.hass.config_entries.async_update_entry(
                self.config_entry, data=new_config
            )

        # Update the serial of the smart key
        smart_key_serial = device_info.get_first_smartkey_serial()
        if smart_key_serial is not None:
            if self.config_entry.data.get(CONF_SERIAL_NUMBER_KEY) != smart_key_serial:
                new_config = self.config_entry.data.copy()
                new_config[CONF_SERIAL_NUMBER_KEY] = smart_key_serial
                self.hass.config_entries.async_update_entry(
                    self.config_entry, data=new_config
                )
        else:
            _LOGGER.debug("No smart keys found for this device.")

    async def _async_update_data(self) -> None:
        """Update data via library (periodic timer)."""
        _LOGGER.debug("async update data")
        try:
            device_info = await self._fetch_data_from_api()
            return device_info
        except ValueError as err:
            raise ConfigEntryAuthFailed from err
