from datetime import date, timedelta
import calendar

# algorytm do obliczenia Wielkanocy

def easter_sunday(year: int) -> date:
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19*a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 22*l) // 451
    month = (h + l - 7*m + 114) // 31
    day = ((h + l - 7*m + 114) % 31) + 1
    return date(year, month, day)


def last_sunday(year: int, month: int) -> date:
    last_day = calendar.monthrange(year, month)[1]
    d = date(year, month, last_day)
    return d - timedelta(days=(d.weekday() - 6) % 7)


def calculate_trading_sundays(year: int) -> list[date]:
    results = set()
    # 1) trzy niedziele przed Wigilią
    wigilia = date(year, 12, 24)
    d = wigilia - timedelta(days=1)
    count = 0
    while count < 3:
        if d.weekday() == 6:
            results.add(d)
            count += 1
        d -= timedelta(days=1)

    # 2) niedziela przed Wielkanocą
    e = easter_sunday(year)
    results.add(e - timedelta(days=7))

    # 3) ostatnie niedziele w styczniu, kwietniu, czerwcu, sierpniu
    # lista świąt
    holidays = {
        date(year, 1, 1), date(year, 1, 6),
        date(year, 5, 1), date(year, 5, 3),
        date(year, 8, 15), date(year, 11, 1),
        date(year, 11, 11), date(year, 12, 25), date(year, 12, 26),
        e, e + timedelta(days=1), e + timedelta(days=49)
    }
    for m in (1, 4, 6, 8):
        s = last_sunday(year, m)
        if s not in holidays:
            results.add(s)

    return sorted(results)