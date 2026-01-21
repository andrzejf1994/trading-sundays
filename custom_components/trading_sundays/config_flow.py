from typing import Any

import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DEFAULT_NAME, DOMAIN
from .translation import async_get_config_entry_title

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("[trading-sundays] Config flow module loaded")


class TradingSundaysFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        _LOGGER.info("[trading-sundays] Config flow step_user started")
        if self._async_current_entries():
            _LOGGER.info("[trading-sundays] Config flow abort: already_configured")
            return self.async_abort(reason="already_configured")
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is None:
            _LOGGER.debug("[trading-sundays] Config flow showing form")
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({}),
                description_placeholders={},
                last_step=True,
            )

        title = await async_get_config_entry_title(self.hass)
        _LOGGER.info("[trading-sundays] Config flow creating entry title=%s", title or DEFAULT_NAME)
        return self.async_create_entry(title=title or DEFAULT_NAME, data={})
