"""Data structures for Flashbird integration."""

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.loader import Integration

from custom_components.flashbird.coordinator import FlashbirdDataUpdateCoordinator

type FlashbirdConfigEntry = ConfigEntry[FlashbirdData]


@dataclass
class FlashbirdData:
    """Data for the integration."""

    coordinator: FlashbirdDataUpdateCoordinator
    integration: Integration
