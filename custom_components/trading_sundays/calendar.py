import logging
from datetime import date, datetime, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DEFAULT_NAME
from .coordinator import TradingSundaysCoordinator
from .translation import async_get_entity_name

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("[trading-sundays] Calendar module loaded")


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> bool:
    coordinator: TradingSundaysCoordinator = hass.data[DOMAIN][entry.entry_id]
    _LOGGER.info(
        "[trading-sundays] Calendar async_setup_entry called entry_id=%s",
        entry.entry_id,
    )
    _LOGGER.debug(
        "[trading-sundays] Calendar coordinator data_count=%s",
        len(coordinator.data or []),
    )
    entities = [TradingSundaysCalendar(coordinator, entry.entry_id)]
    _LOGGER.info(
        "[trading-sundays] Adding calendar entities count=%s",
        len(entities),
    )
    try:
        async_add_entities(entities, True)
    except Exception:
        _LOGGER.exception("[trading-sundays] Adding calendar entities failed")
        raise
    return True


class TradingSundaysCalendar(CoordinatorEntity, CalendarEntity):

    _attr_name = DEFAULT_NAME

    def __init__(self, coordinator: TradingSundaysCoordinator, entry_id: str):
        super().__init__(coordinator)
        self.entity_id = "calendar.trading_sundays"
        self._attr_unique_id = f"{DOMAIN}_{entry_id}_calendar"
        self._event: CalendarEvent | None = None
        _LOGGER.debug("[trading-sundays] Calendar entity initialized")

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        await self._async_set_translated_name()
        self._update_next_event()

    async def _async_set_translated_name(self) -> None:
        name = await async_get_entity_name(self.hass, "calendar", "calendar")
        if name:
            self._attr_name = name
            self.async_write_ha_state()

    @property
    def event(self) -> CalendarEvent | None:
        return self._event

    def _get_event_title(self) -> str:
        lang = self.hass.config.language
        if lang == "pl":
            return "Niedziela Handlowa"
        return "Trading Sunday"

    def _create_event(self, trading_day: date) -> CalendarEvent:
        return CalendarEvent(
            summary=self._get_event_title(),
            start=trading_day,
            end=trading_day + timedelta(days=1),
        )

    def _update_next_event(self):
        today = date.today()
        data = self.coordinator.data or []
        next_trading_day = next((d for d in data if d >= today), None)
        self._event = self._create_event(next_trading_day) if next_trading_day else None
        _LOGGER.debug(
            "[trading-sundays] Next trading Sunday event updated event=%s",
            self._event,
        )

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        start_day = start_date.date()
        end_day = end_date.date()

        data = self.coordinator.data or []
        events = [
            self._create_event(trading_day)
            for trading_day in data
            if start_day <= trading_day <= end_day
        ]
        _LOGGER.debug(
            "[trading-sundays] Calendar requested events between %s and %s found=%d",
            start_day,
            end_day,
            len(events),
        )
        return events

    def _handle_coordinator_update(self):
        self._update_next_event()
        super()._handle_coordinator_update()
        