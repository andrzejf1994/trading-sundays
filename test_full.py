import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'custom_components/trading_sundays'))

from datetime import date
from utils import calculate_trading_sundays

# Test dla konkretnej daty 31.08.2025
sundays = calculate_trading_sundays(2025)
test_date = date(2025, 8, 31)

print(f"Test date: {test_date}")
print(f"All trading Sundays in 2025: {sorted(sundays)}")
print(f"Is trading Sunday: {test_date in sundays}")
