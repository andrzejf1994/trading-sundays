import logging
from datetime import date
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

_LOGGER = logging.getLogger(__name__)

from .const import DOMAIN
from .coordinator import TradingSundaysCoordinator

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: TradingSundaysCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([TradingSundayTodayBinarySensor(coordinator)], True)

class TradingSundayTodayBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Binarny sensor: czy dziś jest niedziela handlowa?"""

    _attr_name = "Is Trading Sunday Today"
    _attr_unique_id = f"{DOMAIN}_today"

    def __init__(self, coordinator: TradingSundaysCoordinator):
        super().__init__(coordinator)
        self._attr_is_on = False

    def _handle_coordinator_update(self):
        today = date.today()
        is_sunday = today.weekday() == 6
        in_trading_sundays = today in self.coordinator.data
        self._attr_is_on = is_sunday and in_trading_sundays
        
        _LOGGER.debug(
            "Binary sensor update - date: %s, is Sunday: %s, in trading Sundays: %s, final state: %s",
            today,
            is_sunday,
            in_trading_sundays,
            self._attr_is_on
        )
        super()._handle_coordinator_update()