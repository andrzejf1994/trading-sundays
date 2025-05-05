import logging
import asyncio
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import TradingSundaysCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration (YAML not used)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Trading Sundays from a config entry."""
    coordinator = TradingSundaysCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Forward setup to sensor and binary_sensor platforms
    await hass.config_entries.async_forward_entry_setup(entry, "sensor")
    await hass.config_entries.async_forward_entry_setup(entry, "binary_sensor")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    # Forward unload to platforms
    unload_sensor = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    unload_binary = await hass.config_entries.async_forward_entry_unload(entry, "binary_sensor")
    unload_ok = unload_sensor and unload_binary
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok