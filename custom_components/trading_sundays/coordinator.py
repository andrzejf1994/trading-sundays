import logging
from datetime import date, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .utils import calculate_trading_sundays

_LOGGER = logging.getLogger(__name__)


class TradingSundaysCoordinator(DataUpdateCoordinator[list[date]]):

    def __init__(self, hass: HomeAssistant) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(days=1),
            update_method=self._async_update_data,
        )

    async def _async_update_data(self) -> list[date]:
        try:
            today = date.today()
            # // Ujednolicone zbieranie dat dla biezacego i nastepnego roku.
            dates: list[date] = []
            for year in (today.year, today.year + 1):
                dates.extend(calculate_trading_sundays(year))
            sorted_dates = sorted(dates)
            _LOGGER.debug(
                "Trading Sundays data updated - today: %s, calculated dates: %s",
                today,
                sorted_dates
            )
            return sorted_dates
        except Exception as err:
            _LOGGER.exception("Error updating trading Sundays")
            raise UpdateFailed(err) from err
