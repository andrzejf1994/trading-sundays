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
    """Binary sensor that indicates if today is a trading Sunday.
    
    This sensor combines two pieces of information:
    1. Whether today is a Sunday
    2. Whether today's date is in the list of trading Sundays
    
    The sensor is ON only when both conditions are true.
    
    State is updated:
    - On initialization
    - When coordinator provides new data
    - Every time the state is accessed through the is_on property
    """

    _attr_name = "Is Trading Sunday Today"
    _attr_unique_id = f"{DOMAIN}_today"

    def __init__(self, coordinator: TradingSundaysCoordinator):
        """Initialize the binary sensor.
        
        Args:
            coordinator: The data coordinator that provides the list of trading Sundays
        """
        _LOGGER.debug("Initializing binary sensor")
        super().__init__(coordinator)
        self._attr_is_on = False
        _LOGGER.debug("Binary sensor initialized with coordinator: %s", coordinator.data)
        # Force initial state update
        self._update_state()

    def _update_state(self):
        """Update the sensor state based on current date and trading Sundays list.
        
        The state is determined by checking if:
        1. Today is a Sunday (weekday == 6)
        2. Today's date exists in the coordinator's trading Sundays list
        
        Both conditions must be true for the sensor to be ON.
        """
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