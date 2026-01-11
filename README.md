# Trading Sundays 🇵🇱

Custom integration for Home Assistant that provides:

- 📅 **Sensor** `sensor.trading_sundays_next` — Displays the date (YYYY-MM-DD) of the next trading (open-for-trade) Sunday in Poland.
- ✅ **Binary Sensor** `binary_sensor.is_trading_sunday_today` — Indicates whether today is a trading Sunday (ON if yes).

This integration follows Home Assistant best practices, using a Config Flow and DataUpdateCoordinator.

---

## Features ⚙️

1. 🛠️ **Config Flow**: Easy UI-based setup (no YAML needed).  
2. 🔄 **Daily Updates**: Automatically recalculates trading Sundays each day.  
3. 🌐 **Translations**: English and Polish language support.

---

## Installation ➕

### Via HACS (recommended) 🏆

1. In Home Assistant sidebar, go to **Settings → Devices & Services → HACS → Integrations**.  
2. Click **+ Add** in the bottom right.  
3. Search for `trading-sundays` or add custom repository URL:

   https://github.com/andrzejf1994/trading-sundays

4. Click **Install** and restart Home Assistant when prompted.

### Manual Installation 🛠️

1. Clone this repository into your `custom_components` folder:

   ```bash
   cd /config/custom_components
   git clone https://github.com/andrzejf1994/trading-sundays.git trading_sundays
   ```

2. Restart Home Assistant.  
3. In the UI, go to **Settings → Devices & Services → Add Integration**, search for **Trading Sundays**, and configure.

---

## Configuration ⚙️

No additional options. The integration automatically calculates all trading Sundays for the current and next year.

---

## Entities 📋

| Entity ID                            | Type          | Description                                   |
| ------------------------------------ | ------------- | --------------------------------------------- |
| `sensor.trading_sundays_next`        | Sensor        | Date of the next trading Sunday (YYYY-MM-DD)  |
| `binary_sensor.trading_sundays_today`| Binary Sensor | ON if today is a trading Sunday               |
| `calendar.trading_sundays_calendar`  | Calendar      | All-day events for every trading Sunday       |

Device classes, icons, and names are localized based on your Home Assistant language.

---

## Development 🛠️

- **Repository**: https://github.com/andrzejf1994/trading-sundays  
- **Branching**: Use `main` for stable releases.  
- **CI/Tests**: GitHub Actions configured for linting and tests.

To test locally:

```bash
cd /config/custom_components/trading_sundays
# make changes
pytest  # run tests
```

---

## Contributing 🤝

1. Fork the repo.  
2. Create a feature branch (`git checkout -b feature/YourFeature`).  
3. Commit your changes (`git commit -m 'Add feature'`).  
4. Push to your branch (`git push origin feature/YourFeature`).  
5. Open a Pull Request.

Please follow Home Assistant developer guidelines.

---

## License 📄

MIT License © 2025 Andrzejf1994
