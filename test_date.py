from datetime import date

def last_sunday(year: int, month: int) -> date:
    from calendar import monthrange
    from datetime import timedelta
    last_day = monthrange(year, month)[1]
    d = date(year, month, last_day)
    return d - timedelta(days=(d.weekday() - 6) % 7)

# Test dla konkretnej daty 31.08.2025
test_date = date(2025, 8, 31)
calculated_date = last_sunday(2025, 8)

print(f"Test date: {test_date}")
print(f"Calculated last Sunday of August 2025: {calculated_date}")
print(f"Is the same date: {test_date == calculated_date}")
print(f"Is Sunday: {test_date.weekday() == 6}")
