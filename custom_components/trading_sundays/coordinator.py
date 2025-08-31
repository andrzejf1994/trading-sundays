import logging
from datetime import date, timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .utils import calculate_trading_sundays

_LOGGER = logging.getLogger(__name__)

class TradingSundaysCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch and update trading Sundays list."""

    def __init__(self, hass):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(days=1),
            update_method=self._async_update_data,
        )

    async def _async_update_data(self):
        try:
            today = date.today()
            dates = calculate_trading_sundays(today.year) + calculate_trading_sundays(today.year + 1)
            sorted_dates = sorted(dates)
            _LOGGER.debug(
                "Trading Sundays data updated - today: %s, calculated dates: %s",
                today,
                sorted_dates
            )
            return sorted_dates
        except Exception as err:
            _LOGGER.error("Error updating trading Sundays: %s", err)
            raise UpdateFailed(err)