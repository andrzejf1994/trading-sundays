import logging
from typing import TYPE_CHECKING

from .const import DOMAIN

if TYPE_CHECKING:  # pragma: no cover
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: "HomeAssistant", config: dict):
    """Set up the integration (YAML not used)."""
    return True

async def async_setup_entry(hass: "HomeAssistant", entry: "ConfigEntry"):
    """Set up Trading Sundays from a config entry."""
    from .coordinator import TradingSundaysCoordinator

    coordinator = TradingSundaysCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Forward setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "binary_sensor", "calendar"])
    return True

async def async_unload_entry(hass: "HomeAssistant", entry: "ConfigEntry"):
    """Unload a config entry."""
    # Forward unload to platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor", "binary_sensor", "calendar"])
    if unload_ok:
        domain_data = hass.data.get(DOMAIN)
        if domain_data is not None:
            domain_data.pop(entry.entry_id, None)
    return unload_ok
