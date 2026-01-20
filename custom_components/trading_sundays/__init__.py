from typing import Any

from .const import DOMAIN, DEFAULT_NAME
from .translation import async_get_config_entry_title

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

PLATFORMS = ("sensor", "binary_sensor", "calendar")

async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    from .coordinator import TradingSundaysCoordinator

    if entry.title == DEFAULT_NAME:
        translated_title = await async_get_config_entry_title(hass)
        if translated_title:
            hass.config_entries.async_update_entry(entry, title=translated_title)

    coordinator = TradingSundaysCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        domain_data = hass.data.get(DOMAIN)
        if domain_data is not None:
            domain_data.pop(entry.entry_id, None)
    return unload_ok
