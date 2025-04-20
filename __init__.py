from .intent import async_register_intents
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    # YAML-alapú beállítás nem támogatott
    return True

async def async_setup_entry(hass, entry):
    await async_register_intents(hass)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    return True

async def async_unload_entry(hass, entry):
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True

async def async_reload_entry(hass, entry):
    _LOGGER.info("Reloading context_provider integration")
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
