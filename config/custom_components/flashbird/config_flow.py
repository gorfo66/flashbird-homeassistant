""" Le Config Flow """

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

from .const import DOMAIN, CONF_NAME


_LOGGER = logging.getLogger(__name__)


class TutoHACSConfigFlow(ConfigFlow, domain=DOMAIN):
    """La classe qui implémente le config flow pour notre DOMAIN.
    Elle doit dériver de FlowHandler"""

    # La version de notre configFlow. Va permettre de migrer les entités
    # vers une version plus récente en cas de changement
    VERSION = 1

    _user_inputs: dict = {}

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Gestion de l'étape 'user'. Point d'entrée de notre
        configFlow. Cette méthode est appelée 2 fois :
        1. une première fois sans user_input -> on affiche le formulaire de configuration
        2. une deuxième fois avec les données saisies par l'utilisateur dans user_input -> on sauvegarde les données saisies
        """
        user_form = vol.Schema(
            {vol.Required("name"): str}
        )

        if user_input is None:
            _LOGGER.debug(
                "config_flow step user (1). 1er appel : pas de user_input -> on affiche le form user_form"
            )
            return self.async_show_form(step_id="user", data_schema=user_form)

        # 2ème appel : il y a des user_input -> on stocke le résultat
        # TODO: utiliser les user_input
        self._user_inputs.update(user_input)

        _LOGGER.debug(
            "config_flow step user (2). On a reçu les valeurs: %s", self._user_inputs
        )

        # On appelle le step 2 ici
        return await self.async_step_2()

    # Cette fois on est libre sur le nommage car ce n'est pas le point d'entrée

    async def async_step_2(self, user_input: dict | None = None) -> FlowResult:
        """Gestion de l'étape 2. Mêmes principes que l'étape user"""
        step2_form = vol.Schema(
            {
                # On attend un entity id du domaine sensor
                vol.Optional("sensor_id"): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain=SENSOR_DOMAIN),
                )
            }
        )

        if user_input is None:
            _LOGGER.debug(
                "config_flow step2 (1). 1er appel : pas de user_input -> "
                "on affiche le form step2_form"
            )
            return self.async_show_form(step_id="2", data_schema=step2_form)

        # 2ème appel : il y a des user_input -> on stocke le résultat
        # TODO: utiliser les user_input
        self._user_inputs.update(user_input)

        _LOGGER.debug(
            "config_flow step2 (2). On a reçu les valeurs: %s", self._user_inputs)
        

        return self.async_create_entry(
            title=self._user_inputs[CONF_NAME], data=self._user_inputs
        )
