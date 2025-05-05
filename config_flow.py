import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, DEFAULT_NAME

class TradingSundaysFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Trading Sundays."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({}),
            )
        return self.async_create_entry(
            title=DEFAULT_NAME,
            data={},
        )