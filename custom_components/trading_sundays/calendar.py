import logging
from datetime import date, datetime, timedelta
from typing import List, Optional

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import TradingSundaysCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up the Trading Sundays calendar entity."""
    coordinator: TradingSundaysCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([TradingSundaysCalendar(coordinator, entry.entry_id)], True)


class TradingSundaysCalendar(CoordinatorEntity, CalendarEntity):
    """Calendar entity exposing trading Sundays as all-day events."""

    _attr_translation_key = "calendar"

    def __init__(self, coordinator: TradingSundaysCoordinator, entry_id: str):
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_{entry_id}_calendar"
        self._event: Optional[CalendarEvent] = None

    async def async_added_to_hass(self):
        """Called when entity is added to Home Assistant."""
        await super().async_added_to_hass()
        self._update_next_event()

    @property
    def event(self) -> Optional[CalendarEvent]:
        """Return the next upcoming trading Sunday as a calendar event."""
        return self._event

    def _get_event_title(self) -> str:
        """Return localized event title based on Home Assistant language."""
        lang = self.hass.config.language
        if lang == "pl":
            return "Niedziela Handlowa"
        return "Trading Sunday"

    def _create_event(self, trading_day: date) -> CalendarEvent:
        """Create an all-day calendar event for a trading Sunday."""
        return CalendarEvent(
            summary=self._get_event_title(),
            start=trading_day,
            end=trading_day + timedelta(days=1),
        )

    def _update_next_event(self):
        """Update the next event based on the coordinator data."""
        today = date.today()
        next_trading_day = next((d for d in self.coordinator.data if d >= today), None)
        self._event = self._create_event(next_trading_day) if next_trading_day else None
        _LOGGER.debug("Next trading Sunday event updated: %s", self._event)

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> List[CalendarEvent]:
        """Return calendar events for trading Sundays within the requested range."""
        start_day = start_date.date()
        end_day = end_date.date()

        events = [
            self._create_event(trading_day)
            for trading_day in self.coordinator.data
            if start_day <= trading_day <= end_day
        ]
        _LOGGER.debug(
            "Calendar requested events between %s and %s: found %d",
            start_day,
            end_day,
            len(events),
        )
        return events

    def _handle_coordinator_update(self):
        """Handle updated data from the coordinator."""
        self._update_next_event()
        super()._handle_coordinator_update()
