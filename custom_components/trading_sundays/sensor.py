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

_LOGGER.debug("[trading-sundays] Sensor module loaded")


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    _LOGGER.info(
        "[trading-sundays] Sensor async_setup_entry called entry_id=%s",
        entry.entry_id,
    )
    coordinator: TradingSundaysCoordinator = hass.data[DOMAIN][entry.entry_id]
    _LOGGER.debug(
        "[trading-sundays] Sensor coordinator data_count=%s",
        len(coordinator.data or []),
    )
    entities = [NextTradingSundaySensor(coordinator)]
    _LOGGER.info(
        "[trading-sundays] Adding sensor entities count=%s",
        len(entities),
    )
    try:
        async_add_entities(entities, False)
    except Exception:
        _LOGGER.exception("[trading-sundays] Adding sensor entities failed")
        raise


class NextTradingSundaySensor(CoordinatorEntity, SensorEntity):
    _attr_name = "Next Trading Sunday"
    _attr_icon = "mdi:calendar-clock"
    _attr_unique_id = f"{DOMAIN}_next"

    def __init__(self, coordinator: TradingSundaysCoordinator):
        super().__init__(coordinator)
        self.entity_id = "sensor.next_trading_sunday"
        self._state: str | None = None
        _LOGGER.debug("[trading-sundays] Sensor entity initialized")

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        await self._async_set_translated_name()

    async def _async_set_translated_name(self) -> None:
        name = await async_get_entity_name(self.hass, "sensor", "next")
        if name:
            self._attr_name = name
            self.async_write_ha_state()
            _LOGGER.debug(
                "[trading-sundays] Sensor translated name applied name=%s",
                name,
            )

    @property
    def native_value(self) -> str | None:
        return self._state

    def _handle_coordinator_update(self):
        today = date.today()
        data = self.coordinator.data or []
        next_date = next((day for day in data if day >= today), None)
        self._state = next_date.isoformat() if next_date else None
        _LOGGER.debug(
            "[trading-sundays] Sensor coordinator update today=%s next_date=%s",
            today,
            next_date,
        )
        super()._handle_coordinator_update()
