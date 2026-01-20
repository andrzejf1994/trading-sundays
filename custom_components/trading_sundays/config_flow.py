from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DEFAULT_NAME, DOMAIN
from .translation import async_get_config_entry_title


class TradingSundaysFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")
        # // Unikalny identyfikator zapobiega duplikatom wpisu.
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({}),
                description_placeholders={},
                last_step=True,
            )

        title = await async_get_config_entry_title(self.hass)
        return self.async_create_entry(title=title or DEFAULT_NAME, data={})
