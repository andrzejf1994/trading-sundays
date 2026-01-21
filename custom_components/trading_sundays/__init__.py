from typing import Any

import logging

from .const import DOMAIN, DEFAULT_NAME
from .translation import async_get_config_entry_title

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ("sensor", "binary_sensor", "calendar")

_LOGGER.debug("[trading-sundays] Module loaded")

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    from .coordinator import TradingSundaysCoordinator

    _LOGGER.info(
        "[trading-sundays] async_setup_entry called entry_id=%s title=%s",
        entry.entry_id,
        entry.title,
    )
    _LOGGER.debug(
        "[trading-sundays] Config entry data keys=%s options keys=%s",
        list(entry.data.keys()),
        list(entry.options.keys()),
    )
    if entry.title == DEFAULT_NAME:
        translated_title = await async_get_config_entry_title(hass)
        if translated_title:
            _LOGGER.debug(
                "[trading-sundays] Updating entry title to translated value: %s",
                translated_title,
            )
            hass.config_entries.async_update_entry(entry, title=translated_title)

    try:
        coordinator = TradingSundaysCoordinator(hass)
        _LOGGER.debug(
            "[trading-sundays] Coordinator created update_interval=%s",
            coordinator.update_interval,
        )
        await coordinator.async_config_entry_first_refresh()
        _LOGGER.info(
            "[trading-sundays] Coordinator first refresh complete data_count=%s",
            len(coordinator.data or []),
        )
    except Exception:
        _LOGGER.exception("[trading-sundays] Coordinator setup or first refresh failed")
        raise

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    _LOGGER.info(
        "[trading-sundays] Forwarding entry setups for platforms=%s",
        PLATFORMS,
    )
    try:
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    except Exception:
        _LOGGER.exception("[trading-sundays] Platform forwarding failed")
        raise
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.info(
        "[trading-sundays] async_unload_entry called entry_id=%s", entry.entry_id
    )
    try:
        unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    except Exception:
        _LOGGER.exception("[trading-sundays] Platform unload failed")
        raise
    if unload_ok:
        domain_data = hass.data.get(DOMAIN)
        if domain_data is not None:
            domain_data.pop(entry.entry_id, None)
    _LOGGER.info(
        "[trading-sundays] async_unload_entry finished entry_id=%s unload_ok=%s",
        entry.entry_id,
        unload_ok,
    )
    return unload_ok
