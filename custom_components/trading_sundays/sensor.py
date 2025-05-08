import logging
from datetime import date
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import TradingSundaysCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities: AddEntitiesCallback):
    coordinator: TradingSundaysCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NextTradingSundaySensor(coordinator)], False)

class NextTradingSundaySensor(CoordinatorEntity, SensorEntity):
    """Sensor zwracający datę najbliższej niedzieli handlowej."""

    _attr_name = "Next Trading Sunday"
    _attr_icon = "mdi:calendar-clock"
    _attr_unique_id = f"{DOMAIN}_next"

    def __init__(self, coordinator: TradingSundaysCoordinator):
        super().__init__(coordinator)
        self._state = None

    @property
    def native_value(self):
        return self._state

    def _handle_coordinator_update(self):
        today = date.today()
        for d in self.coordinator.data:
            if d >= today:
                self._state = d.isoformat()
                break
        super()._handle_coordinator_update()