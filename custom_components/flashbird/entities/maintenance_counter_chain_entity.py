"""Entity for the maintenance counter chain."""

import logging

from homeassistant.components.sensor import (
    RestoreSensor,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import UnitOfLength
from homeassistant.core import HomeAssistant

from custom_components.flashbird.const import EVENT_RESET_COUNTER
from custom_components.flashbird.data import FlashbirdConfigEntry
from custom_components.flashbird.entities.abstract_flashbird_sensor_entity import (
    AbstractFlashbirdSensorEntity,
)

_LOGGER = logging.getLogger(__name__)


class FlashbirdMaintenanceCounterChainEntity(
    AbstractFlashbirdSensorEntity, RestoreSensor
):
    """Accumulated maintenance counter chain using computed increments."""

    _logger = logging.getLogger(__name__)

    def __init__(self, hass: HomeAssistant, config_entry: FlashbirdConfigEntry) -> None:
        """Create the maintenance counter chain entity."""
        super().__init__(hass, config_entry)
        self._attr_unique_id = self._config.entry_id + "_maintenance_counter_chain"
        self._attr_translation_key = "maintenance_counter_chain"

        # Listen for reset event sent from the button.
        self._hass.bus.async_listen(EVENT_RESET_COUNTER, self._async_handle_reset_event)

    @property
    def icon(self) -> str | None:
        """Return the icon for the entity."""
        return "mdi:counter"

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the device class."""
        return SensorDeviceClass.DISTANCE

    @property
    def state_class(self) -> SensorStateClass | None:
        """Return the state class."""
        return SensorStateClass.TOTAL_INCREASING

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the native unit of measurement."""
        return UnitOfLength.KILOMETERS

    @property
    def suggested_display_precision(self) -> int:
        """Return the suggested precision."""
        return 0

    async def async_added_to_hass(self) -> None:
        """
        Override to manage restore state.

        This method is called by the framework when an entity has their entity_id and
        hass object assigned, before it is written to the state machine for the first time.
        """
        await super().async_added_to_hass()

        # Manage restore state
        initial_value = 0
        restored_data = await self.async_get_last_sensor_data()
        if restored_data is not None and restored_data.native_value is not None:
            initial_value = restored_data.native_value
        self._attr_native_value = initial_value

    async def _async_handle_reset_event(self, event: any) -> None:
        """Reset the sensor to zero."""
        device_id = event.data.get("device_id")
        if device_id == self.unique_id:
            self._logger.debug("reset %s", device_id)
            if self.native_value is None or self.native_value > 0:
                self._attr_native_value = 0
                await self.async_write_ha_state()

    def _get_updated_data(self) -> int | None:
        """Return the new incremented value or None if the increment is 0."""
        device_info = self._get_flashbird_device_info()
        increment = round(device_info.get_mileage_increment() / 1000)  # convert in km
        if increment > 0 and self.native_value is not None:
            current = self.native_value
            return current + int(increment)

        return None
