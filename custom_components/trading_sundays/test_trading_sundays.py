from datetime import date

from .utils import calculate_trading_sundays

def test_august_2025():
    # Test dla konkretnej daty 31.08.2025
    sundays = calculate_trading_sundays(2025)
    test_date = date(2025, 8, 31)
    
    # Sprawdź czy 31.08.2025 jest w liście handlowych niedziel
    assert test_date in sundays, f"31.08.2025 should be a trading Sunday, but isn't in the list: {sundays}"
