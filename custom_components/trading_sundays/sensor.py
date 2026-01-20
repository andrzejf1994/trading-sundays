import logging
from datetime import date

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import TradingSundaysCoordinator
from .translation import async_get_entity_name

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: TradingSundaysCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NextTradingSundaySensor(coordinator)], False)


class NextTradingSundaySensor(CoordinatorEntity, SensorEntity):
    _attr_name = "Next Trading Sunday"
    _attr_icon = "mdi:calendar-clock"
    _attr_unique_id = f"{DOMAIN}_next"

    def __init__(self, coordinator: TradingSundaysCoordinator):
        super().__init__(coordinator)
        self.entity_id = "sensor.next_trading_sunday"
        self._state: str | None = None

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        await self._async_set_translated_name()

    async def _async_set_translated_name(self) -> None:
        name = await async_get_entity_name(self.hass, "sensor", "next")
        if name:
            self._attr_name = name
            self.async_write_ha_state()

    @property
    def native_value(self) -> str | None:
        return self._state

    def _handle_coordinator_update(self):
        today = date.today()
        # // Lokalna zmienna ogranicza powtorne odwolania do koordynatora.
        data = self.coordinator.data or []
        next_date = next((day for day in data if day >= today), None)
        self._state = next_date.isoformat() if next_date else None
        super()._handle_coordinator_update()
