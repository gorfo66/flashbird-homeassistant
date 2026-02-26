"""Button to reset the maintenance counter chain."""

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo

from custom_components.flashbird.const import EVENT_RESET_COUNTER
from custom_components.flashbird.data import FlashbirdConfigEntry
from custom_components.flashbird.helpers.device_info import define_device_info


class FlashbirdMaintenanceCounterChainResetButtonEntity(ButtonEntity):
    """Button entity that resets the maintenance counter chain."""

    _logger = logging.getLogger(__name__)

    def __init__(self, hass: HomeAssistant, config_entry: FlashbirdConfigEntry) -> None:
        """Create the reset maintenance counter chain button."""
        self._hass = hass
        self._config = config_entry
        self._attr_has_entity_name = True
        self._attr_unique_id = (
            self._config.entry_id + "_maintenance_counter_chain_reset_button"
        )
        self._attr_translation_key = "reset_maintenance_counter_chain"

    @property
    def icon(self) -> str | None:
        """Return the icon for the entity."""
        return "mdi:restore"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for the entity."""
        return define_device_info(self._config)

    def press(self) -> None:
        """Reset the counter value and set last_reset to now."""
        self._logger.debug("Button pressed")
        self._hass.bus.fire(
            EVENT_RESET_COUNTER,
            {"device_id": self._config.entry_id + "_maintenance_counter_chain"},
        )
