# Trading Sundays <img src="assets/icons/icon.png" alt="Trading Sundays" height="32">

Custom integration for Home Assistant that provides:

- **Sensor** `sensor.trading_sundays_next` — Displays the date (YYYY-MM-DD) of the next trading (open-for-trade) Sunday in Poland.
- **Binary Sensor** `binary_sensor.is_trading_sunday_today` — Indicates whether today is a trading Sunday (ON if yes).

This integration follows Home Assistant best practices, using a Config Flow and DataUpdateCoordinator.

---

## Features

1. **Config Flow**: Easy UI-based setup (no YAML needed).  
2. **Daily Updates**: Automatically recalculates trading Sundays each day.  
3. **Translations**: English and Polish language support.

---

## Installation

### Via HACS

1. In Home Assistant sidebar, go to **Settings → Devices & Services → HACS → Integrations**.  
2. Click **+ Add** in the bottom right.  
3. Search for `trading-sundays` or add custom repository URL:
   
   [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=andrzejf1994&repository=trading-sundays&category=integration)

4. Click **Install** and restart Home Assistant when prompted.

---

## Configuration

No additional options. The integration automatically calculates all trading Sundays for the current and next year.

---

## Entities

| Entity ID                            | Type          | Description                                   |
| ------------------------------------ | ------------- | --------------------------------------------- |
| `sensor.trading_sundays_next`        | Sensor        | Date of the next trading Sunday (YYYY-MM-DD)  |
| `binary_sensor.trading_sundays_today`| Binary Sensor | ON if today is a trading Sunday               |
| `calendar.trading_sundays`  | Calendar      | All-day events for every trading Sunday       |

Device classes, icons, and names are localized based on your Home Assistant language.

## License

MIT License © 2025 andrzejf1994
