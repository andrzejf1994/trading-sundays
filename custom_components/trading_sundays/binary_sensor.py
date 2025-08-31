import logging
from datetime import date
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

_LOGGER = logging.getLogger(__name__)

from .const import DOMAIN
from .coordinator import TradingSundaysCoordinator

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: TradingSundaysCoordinator = hass.data[DOMAIN][entry.entry_id]
    _LOGGER.debug("Setting up binary sensor with coordinator data: %s", coordinator.data)
    async_add_entities([TradingSundayTodayBinarySensor(coordinator)], True)

class TradingSundayTodayBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Binarny sensor: czy dziś jest niedziela handlowa?"""

    _attr_name = "Is Trading Sunday Today"
    _attr_unique_id = f"{DOMAIN}_today"

    def __init__(self, coordinator: TradingSundaysCoordinator):
        _LOGGER.debug("Initializing binary sensor")
        super().__init__(coordinator)
        self._attr_is_on = False
        _LOGGER.debug("Binary sensor initialized with coordinator: %s", coordinator.data)
        # Wymuszamy pierwszą aktualizację stanu
        self._update_state()

    def _update_state(self):
        """Update sensor state."""
        today = date.today()
        is_sunday = today.weekday() == 6
        in_trading_sundays = today in self.coordinator.data
        
        old_state = self._attr_is_on
        self._attr_is_on = is_sunday and in_trading_sundays
        
        _LOGGER.debug(
            "Binary sensor state update - date: %s, is Sunday: %s, in trading Sundays: %s, state changed: %s -> %s",
            today,
            is_sunday,
            in_trading_sundays,
            old_state,
            self._attr_is_on
        )

    @property
    def is_on(self):
        """Return the state of the binary sensor."""
        self._update_state()
        _LOGGER.debug("Binary sensor is_on property accessed, returning: %s", self._attr_is_on)
        return self._attr_is_on

    def _handle_coordinator_update(self):
        """Handle updated data from the coordinator."""
        _LOGGER.debug("Binary sensor handling coordinator update")
        self._update_state()
        super()._handle_coordinator_update()