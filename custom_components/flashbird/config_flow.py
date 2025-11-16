"""Config flow for the Flashbird integration."""

import logging
from typing import ClassVar

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.core import HomeAssistantError, callback
from homeassistant.data_entry_flow import FlowResult

from custom_components.flashbird.const import (
    CONF_FIRMWARE_VERSION,
    CONF_MANUFACTURER,
    CONF_MODEL,
    CONF_NAME,
    CONF_SERIAL_NUMBER,
    CONF_TOKEN,
    CONF_TRACKER_ID,
    DOMAIN,
)
from custom_components.flashbird.helpers.flashbird_api import (
    flashbird_find_device_id,
    flashbird_get_device_info,
    flashbird_get_token,
)

_LOGGER = logging.getLogger(__name__)


class FlashbirdConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Flashbird."""

    VERSION = 1

    _config: ClassVar[dict] = {}

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle the initial step of the user flow."""
        user_form = vol.Schema(
            {
                vol.Required("email"): str,
                vol.Required("password"): str,
                vol.Required("name"): str,
                vol.Required("serial"): str,
            }
        )

        # if no data, show the form
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=user_form)

        # process the data

        try:
            token = await self.hass.async_add_executor_job(
                flashbird_get_token, user_input["email"], user_input["password"]
            )
        except ValueError as err:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="invalid_token",
                translation_placeholders=None,
            ) from err

        serial = user_input["serial"]
        tracker_id = await self.hass.async_add_executor_job(
            flashbird_find_device_id, token, serial
        )
        if tracker_id is None:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="invalid_serial_number",
                translation_placeholders=None,
            )

        device_info = await self.hass.async_add_executor_job(
            flashbird_get_device_info, token, tracker_id
        )
        self._config[CONF_TOKEN] = token
        self._config[CONF_SERIAL_NUMBER] = serial
        self._config[CONF_TRACKER_ID] = tracker_id
        self._config[CONF_MANUFACTURER] = "SMT Performances"
        self._config[CONF_MODEL] = device_info.get_device_type().capitalize()
        self._config[CONF_NAME] = user_input["name"]
        self._config[CONF_FIRMWARE_VERSION] = ""

        return self.async_create_entry(title=serial, data=self._config)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> "FlashbirdOptionsFlow":
        """Get options flow for this handler."""
        return FlashbirdOptionsFlow(config_entry)

    async def async_step_reauth(self, entry_data: dict) -> FlowResult:
        """Perform reauth upon an API authentication error."""
        # entry_data is required by the signature but not used.
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Show dialog that informs the user that reauth is required."""
        reauth_form = vol.Schema(
            {
                vol.Required("email"): str,
                vol.Required("password"): str,
            }
        )

        # if no data, show the form
        if user_input is None:
            return self.async_show_form(
                step_id="reauth_confirm", data_schema=reauth_form
            )

        # process the data
        try:
            token = await self.hass.async_add_executor_job(
                flashbird_get_token, user_input["email"], user_input["password"]
            )
            newConfig = self._config.data.copy()
            newConfig[CONF_TOKEN] = token

            self.hass.config_entries.async_update_entry(self._config, data=newConfig)
            return self.async_update_reload_and_abort(title=None, data=None)
        except ValueError:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="invalid_token",
                translation_placeholders=None,
            )


class FlashbirdOptionsFlow(OptionsFlow):
    """Options flow for Flashbird integration."""

    _config: ConfigEntry = None

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self._config = config_entry

    async def async_step_init(self, user_input: dict | None = None) -> FlowResult:
        """Handle the initial step of the options flow."""
        option_form = vol.Schema(
            {
                vol.Required("email"): str,
                vol.Required("password"): str,
            }
        )
        if user_input is None:
            return self.async_show_form(step_id="init", data_schema=option_form)
        try:
            token = await self.hass.async_add_executor_job(
                flashbird_get_token, user_input["email"], user_input["password"]
            )
            new_config = self._config.data.copy()
            new_config[CONF_TOKEN] = token
            self.hass.config_entries.async_update_entry(self._config, data=new_config)
            return self.async_create_entry(title=None, data=None)
        except ValueError as err:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="invalid_token",
                translation_placeholders=None,
            ) from err
