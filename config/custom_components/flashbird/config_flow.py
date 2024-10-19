import logging
from typing import Any
import copy
from collections.abc import Mapping

from homeassistant.core import callback
from homeassistant.config_entries import ConfigFlow, OptionsFlow, ConfigEntry
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN

import voluptuous as vol

from .const import DOMAIN, CONF_SERIAL_NUMBER, CONF_TOKEN, CONF_TRACKER_ID, CONF_MANUFACTURER, CONF_MODEL
from .helpers.flashbird_api import flashbird_get_token, flashbird_find_device_id, flashbird_get_device_info


_LOGGER = logging.getLogger(__name__)


class FlashbirdConfigFlow(ConfigFlow, domain=DOMAIN):
    
    VERSION = 1

    _config: dict = {}

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        
        user_form = vol.Schema(
          {
            vol.Required("email"): str,
            vol.Required("password"): str,
            vol.Required("serial"): str
          }
        )

        # if no data, show the form
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=user_form)


        # process the data
        token = await self.hass.async_add_executor_job(flashbird_get_token, user_input['email'], user_input['password'])
        serial = user_input['serial']
        trackerId = await self.hass.async_add_executor_job(flashbird_find_device_id, token, serial)
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