from datetime import date
from homeassistant.components.binary_sensor import BinarySensorEntity, DEVICE_CLASS_RUNNING
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import TradingSundaysCoordinator

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: TradingSundaysCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([TradingSundayTodayBinarySensor(coordinator)], False)

class TradingSundayTodayBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Binarny sensor: czy dziś jest niedziela handlowa?"""

    _attr_name = "Is Trading Sunday Today"
    _attr_device_class = DEVICE_CLASS_RUNNING
    _attr_unique_id = f"{DOMAIN}_today"

    def __init__(self, coordinator: TradingSundaysCoordinator):
        super().__init__(coordinator)
        self._attr_is_on = False

    def _handle_coordinator_update(self):
        today = date.today()
        self._attr_is_on = (today.weekday() == 6 and today in self.coordinator.data)
        super()._handle_coordinator_update()