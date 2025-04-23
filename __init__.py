import logging
import shutil
from .intent import async_register_intents
from .const import DOMAIN
from .prompt_builder import build_prompt_context
from .utils.rendered_output import write_rendered_topics_md
from homeassistant.components import panel_custom
from homeassistant.components.http import StaticPathConfig

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """Set up the context_provider integration."""
    # await panel_custom.async_register_panel(
    #     hass=hass,
    #     frontend_url_path="topic-editor",
    #     webcomponent_name="topic_editor",
    #     sidebar_title="Topic szerkesztő",
    #     sidebar_icon="mdi:book-edit",
    #     module_url="/api/context_provider/static/topic_editor.js?v=6",
    #     require_admin=False,
    # )
    # _LOGGER.debug("Registering static path for topic_editor.js")
    # await hass.http.async_register_static_paths(
    #     [
    #         StaticPathConfig(
    #             "/api/context_provider/static/topic_editor.js",
    #             hass.config.path(
    #                 "custom_components/context_provider/www/topic_editor.js"
    #             ),
    #             False,
    #         )
    #     ]
    # )

    # _LOGGER.debug("Static path registered successfully")
    return True


async def async_setup_entry(hass, entry):
    """Set up a config entry for context_provider."""
    _LOGGER.info("Setting up context_provider entry")

    # Register intents
    await async_register_intents(hass)

    # Build dynamic context for prompt rendering
    prompt_context = await build_prompt_context()

    # Store data in hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["prompt_context"] = prompt_context
    hass.data[DOMAIN][entry.entry_id] = entry.data
    # Save markdown file
    await write_rendered_topics_md(prompt_context.get("topics", {}))

    # Forward setup to the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True


async def async_unload_entry(hass, entry):
    """Unload a config entry for context_provider."""
    _LOGGER.info("Unloading context_provider entry")

    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    hass.data[DOMAIN].pop(entry.entry_id, None)

    # Cleanup if no more entries left
    if not hass.data[DOMAIN]:
        hass.data.pop(DOMAIN)

    return True


async def async_reload_entry(hass, entry):
    """Reload a config entry for context_provider."""
    _LOGGER.info("Reloading context_provider integration")
    await async_unload_entry(hass, entry)
    return await async_setup_entry(hass, entry)


async def async_setup_intents(hass):
    """Set up intents for the context_provider integration."""
    _LOGGER.debug("Setting up intents for context_provider")
    await async_register_intents(hass)
