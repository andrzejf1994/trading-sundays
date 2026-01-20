from homeassistant.core import HomeAssistant
from homeassistant.helpers.translation import async_get_translations

from .const import DOMAIN


async def _async_get_translation(
    hass: HomeAssistant, category: str, translation_key: str
) -> str | None:
    # // Wspolna funkcja ogranicza duplikacje kodu.
    translations = await async_get_translations(
        hass,
        hass.config.language,
        category,
        [DOMAIN],
    )
    return translations.get(translation_key)


async def async_get_entity_name(
    hass: HomeAssistant, platform: str, key: str
) -> str | None:
    translation_key = f"component.{DOMAIN}.entity.{platform}.{key}.name"
    return await _async_get_translation(hass, "entity", translation_key)


async def async_get_config_entry_title(hass: HomeAssistant) -> str | None:
    translation_key = f"component.{DOMAIN}.title"
    return await _async_get_translation(hass, "title", translation_key)
