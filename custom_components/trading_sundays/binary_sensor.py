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

_LOGGER.debug("[trading-sundays] Binary sensor module loaded")


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: TradingSundaysCoordinator = hass.data[DOMAIN][entry.entry_id]
    _LOGGER.info(
        "[trading-sundays] Binary sensor async_setup_entry called entry_id=%s",
        entry.entry_id,
    )
    _LOGGER.debug(
        "[trading-sundays] Setting up binary sensor with coordinator data_count=%s",
        len(coordinator.data or []),
    )
    entities = [TradingSundayTodayBinarySensor(coordinator)]
    _LOGGER.info(
        "[trading-sundays] Adding binary sensor entities count=%s",
        len(entities),
    )
    try:
        async_add_entities(entities, True)
    except Exception:
        _LOGGER.exception("[trading-sundays] Adding binary sensor entities failed")
        raise


class TradingSundayTodayBinarySensor(CoordinatorEntity, BinarySensorEntity):
    _attr_name = "Is Trading Sunday Today"
    _attr_unique_id = f"{DOMAIN}_today"

    def __init__(self, coordinator: TradingSundaysCoordinator):
        _LOGGER.debug("[trading-sundays] Initializing binary sensor")
        super().__init__(coordinator)
        self.entity_id = "binary_sensor.is_trading_sunday_today"
        self._attr_is_on = False
        _LOGGER.debug(
            "[trading-sundays] Binary sensor initialized with coordinator data_count=%s",
            len(coordinator.data or []),
        )
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
        data = self.coordinator.data or []
        in_trading_sundays = today in data

        old_state = self._attr_is_on
        self._attr_is_on = is_sunday and in_trading_sundays

        _LOGGER.debug(
            "[trading-sundays] Binary sensor state update - date=%s is_sunday=%s in_trading_sundays=%s state_changed=%s->%s",
            today,
            is_sunday,
            in_trading_sundays,
            old_state,
            self._attr_is_on
        )

    @property
    def is_on(self) -> bool:
        self._update_state()
        _LOGGER.debug(
            "[trading-sundays] Binary sensor is_on accessed returning=%s",
            self._attr_is_on,
        )
        return self._attr_is_on

    def _handle_coordinator_update(self):
        _LOGGER.debug("[trading-sundays] Binary sensor handling coordinator update")
        self._update_state()
        super()._handle_coordinator_update()
