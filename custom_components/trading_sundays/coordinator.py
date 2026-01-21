import logging
from datetime import date, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .utils import calculate_trading_sundays

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("[trading-sundays] Coordinator module loaded")


class TradingSundaysCoordinator(DataUpdateCoordinator[list[date]]):

    def __init__(self, hass: HomeAssistant) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(days=1),
            update_method=self._async_update_data,
        )
        _LOGGER.debug(
            "[trading-sundays] Coordinator initialized update_interval=%s",
            self.update_interval,
        )

    async def _async_update_data(self) -> list[date]:
        try:
            _LOGGER.debug("[trading-sundays] Coordinator update started")
            today = date.today()
            dates: list[date] = []
            for year in (today.year, today.year + 1):
                dates.extend(calculate_trading_sundays(year))
            sorted_dates = sorted(dates)
            _LOGGER.debug(
                "[trading-sundays] Data updated - today=%s calculated_dates=%s",
                today,
                sorted_dates
            )
            return sorted_dates
        except Exception as err:
            _LOGGER.exception("[trading-sundays] Error updating trading Sundays")
            raise UpdateFailed(err) from err
