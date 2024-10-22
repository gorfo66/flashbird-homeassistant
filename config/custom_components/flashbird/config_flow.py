import logging

from homeassistant.core import callback, HomeAssistantError
from homeassistant.config_entries import ConfigFlow, OptionsFlow, ConfigEntry
from homeassistant.data_entry_flow import FlowResult

import voluptuous as vol

from .const import DOMAIN, CONF_SERIAL_NUMBER, CONF_TOKEN, CONF_TRACKER_ID, CONF_MANUFACTURER, CONF_MODEL
from .helpers.flashbird_api import flashbird_get_token, flashbird_find_device_id, flashbird_get_device_info


_LOGGER = logging.getLogger(__name__)


class FlashbirdConfigFlow(ConfigFlow, domain=DOMAIN):

    VERSION = 1

    _config: dict = {}

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        user_form = vol.Schema({
            vol.Required("email"): str,
            vol.Required("password"): str,
            vol.Required("serial"): str
        }
        )

        # if no data, show the form
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=user_form)

        # process the data

        try:
            token = await self.hass.async_add_executor_job(flashbird_get_token, user_input['email'], user_input
                                                           ['password'])
        except ValueError:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="invalid_token",
                translation_placeholders=None
            )

        serial = user_input['serial']
        trackerId = await self.hass.async_add_executor_job(flashbird_find_device_id, token, serial)
        if (trackerId == None):
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="invalid_serial_number",
                translation_placeholders=None
            )

        deviceInfo = await self.hass.async_add_executor_job(flashbird_get_device_info, token, trackerId)
        self._config[CONF_TOKEN] = token
        self._config[CONF_SERIAL_NUMBER] = serial
        self._config[CONF_TRACKER_ID] = trackerId
        self._config[CONF_MANUFACTURER] = deviceInfo['motorcycle']['brand']['label']
        self._config[CONF_MODEL] = deviceInfo['motorcycle']['model']['label']

        return self.async_create_entry(
            title=serial,
            data=self._config
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry):
        """Get options flow for this handler"""
        return FlashbirdOptionsFlow(config_entry)


class FlashbirdOptionsFlow(OptionsFlow):

    _config: ConfigEntry = None

    def __init__(self, config_entry: ConfigEntry) -> None:
        self._config = config_entry

    async def async_step_init(self, user_input: dict | None = None) -> FlowResult:
        option_form = vol.Schema({
            vol.Required("email"): str,
            vol.Required("password"): str,
        })

        # if no data, show the form
        if user_input is None:
            return self.async_show_form(step_id="init", data_schema=option_form)

        # process the data
        try:
            token = await self.hass.async_add_executor_job(flashbird_get_token, user_input['email'], user_input['password'])
            newConfig = self._config.data.copy()
            newConfig[CONF_TOKEN] = token

            self.hass.config_entries.async_update_entry(
                self._config, data=newConfig)
            return self.async_create_entry(title=None, data=None)
        except ValueError:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="invalid_token",
                translation_placeholders=None
            )
