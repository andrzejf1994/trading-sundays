"""Unit tests for Trading Sundays integration."""
import pytest
from datetime import date
from unittest.mock import MagicMock, patch
from homeassistant.core import HomeAssistant
from custom_components.trading_sundays.binary_sensor import TradingSundayTodayBinarySensor
from custom_components.trading_sundays.coordinator import TradingSundaysCoordinator

@pytest.fixture
def hass():
    """Return a mock Home Assistant instance."""
    return MagicMock(spec=HomeAssistant)

@pytest.fixture
def coordinator(hass):
    """Return a mock coordinator instance."""
    coordinator = TradingSundaysCoordinator(hass)
    coordinator.data = [
        date(2025, 8, 31),  # Last Sunday of August 2025
        date(2025, 12, 21),  # Sunday before Christmas 2025
    ]
    return coordinator

def test_binary_sensor_init(coordinator):
    """Test binary sensor initialization."""
    sensor = TradingSundayTodayBinarySensor(coordinator)
    assert sensor._attr_name == "Is Trading Sunday Today"
    assert not sensor._attr_is_on  # Should be False by default

@patch('custom_components.trading_sundays.binary_sensor.date')
def test_binary_sensor_trading_sunday(mock_date, coordinator):
    """Test binary sensor on a trading Sunday."""
    mock_date.today.return_value = date(2025, 8, 31)  # Trading Sunday
    sensor = TradingSundayTodayBinarySensor(coordinator)
    assert sensor.is_on

@patch('custom_components.trading_sundays.binary_sensor.date')
def test_binary_sensor_non_trading_sunday(mock_date, coordinator):
    """Test binary sensor on a non-trading Sunday."""
    mock_date.today.return_value = date(2025, 8, 24)  # Non-trading Sunday
    sensor = TradingSundayTodayBinarySensor(coordinator)
    assert not sensor.is_on

@patch('custom_components.trading_sundays.binary_sensor.date')
def test_binary_sensor_not_sunday(mock_date, coordinator):
    """Test binary sensor on a non-Sunday."""
    mock_date.today.return_value = date(2025, 8, 30)  # Saturday
    sensor = TradingSundayTodayBinarySensor(coordinator)
    assert not sensor.is_on
