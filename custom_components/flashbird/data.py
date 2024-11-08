from homeassistant.loader import Integration
from dataclasses import dataclass
from .coordinator import FlashbirdDataUpdateCoordinator
from homeassistant.config_entries import ConfigEntry

type FlashbirdConfigEntry = ConfigEntry[FlashbirdData]


@dataclass
class FlashbirdData:
    """Data for the integration."""

    coordinator: FlashbirdDataUpdateCoordinator
    integration: Integration
