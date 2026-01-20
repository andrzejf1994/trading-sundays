import logging
from datetime import date

from homeassistant.components.binary_sensor import BinarySensorEntity
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
    _LOGGER.debug("Setting up binary sensor with coordinator data: %s", coordinator.data)
    async_add_entities([TradingSundayTodayBinarySensor(coordinator)], True)


class TradingSundayTodayBinarySensor(CoordinatorEntity, BinarySensorEntity):
    _attr_name = "Is Trading Sunday Today"
    _attr_unique_id = f"{DOMAIN}_today"

    def __init__(self, coordinator: TradingSundaysCoordinator):
        _LOGGER.debug("Initializing binary sensor")
        super().__init__(coordinator)
        self.entity_id = "binary_sensor.is_trading_sunday_today"
        self._attr_is_on = False
        _LOGGER.debug("Binary sensor initialized with coordinator: %s", coordinator.data)
        self._update_state()

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        await self._async_set_translated_name()

    async def _async_set_translated_name(self) -> None:
        name = await async_get_entity_name(self.hass, "binary_sensor", "today")
        if name:
            self._attr_name = name
            self.async_write_ha_state()

    def _update_state(self):
        today = date.today()
        is_sunday = today.weekday() == 6
        # // Obrona przed None w danych koordynatora.
        data = self.coordinator.data or []
        in_trading_sundays = today in data

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
    def is_on(self) -> bool:
        # // Zachowano odswiezanie stanu przy odczycie wlasciwosci.
        self._update_state()
        _LOGGER.debug("Binary sensor is_on property accessed, returning: %s", self._attr_is_on)
        return self._attr_is_on

    def _handle_coordinator_update(self):
        _LOGGER.debug("Binary sensor handling coordinator update")
        self._update_state()
        super()._handle_coordinator_update()
