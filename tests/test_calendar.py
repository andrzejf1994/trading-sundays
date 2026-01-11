"""Tests for the Trading Sundays calendar entity."""
from datetime import date as real_date, datetime
from unittest.mock import MagicMock, patch

import pytest

pytest.importorskip("homeassistant")
from homeassistant.core import HomeAssistant  # noqa: E402

from custom_components.trading_sundays.calendar import TradingSundaysCalendar  # noqa: E402
from custom_components.trading_sundays.coordinator import TradingSundaysCoordinator  # noqa: E402


@pytest.fixture
def hass():
    """Return a mock Home Assistant instance."""
    return MagicMock(spec=HomeAssistant)


@pytest.fixture
def coordinator(hass):
    """Return a mock coordinator instance with sample data."""
    coordinator = TradingSundaysCoordinator(hass)
    coordinator.data = [
        real_date(2025, 8, 31),
        real_date(2025, 12, 21),
    ]
    return coordinator


@patch("custom_components.trading_sundays.calendar.date")
def test_calendar_event_all_day(mock_date, coordinator):
    """Ensure the next event is an all-day entry on the next trading Sunday."""
    mock_date.side_effect = lambda *args, **kwargs: real_date(*args, **kwargs)
    mock_date.today.return_value = real_date(2025, 8, 24)

    calendar_entity = TradingSundaysCalendar(coordinator, "test_entry")

    assert calendar_entity.event is not None
    assert calendar_entity.event.start == real_date(2025, 8, 31)
    assert calendar_entity.event.end == real_date(2025, 9, 1)
    assert calendar_entity.event.all_day
    assert calendar_entity.unique_id == "trading_sundays_test_entry_calendar"


@pytest.mark.asyncio
async def test_calendar_events_range(coordinator, hass):
    """Ensure events are returned for trading Sundays in the requested range."""
    calendar_entity = TradingSundaysCalendar(coordinator, "test_entry")

    events = await calendar_entity.async_get_events(
        hass,
        datetime(2025, 8, 1),
        datetime(2025, 12, 31),
    )

    assert len(events) == 2
    assert events[0].start == real_date(2025, 8, 31)
    assert events[1].start == real_date(2025, 12, 21)
