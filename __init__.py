import logging
import os
import shutil
from pathlib import Path

from homeassistant.components import panel_custom
from homeassistant.components.http import StaticPathConfig


from .intent import async_register_intents
from .const import DOMAIN
from .prompt_builder import build_prompt_context
from .helpers.rendered_output import write_rendered_topics_md

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """Set up the context_provider integration."""

    # (Ha újra aktiválnád a panel_custom-ot, ez itt van kikommentezve.)
    # await panel_custom.async_register_panel(
    #     hass=hass,
    #     frontend_url_path="topic-editor",
    #     webcomponent_name="topic_editor",
    #     sidebar_title="Topic szerkesztő",
    #     sidebar_icon="mdi:book-edit",
    #     module_url="/api/context_provider/static/topic_editor.js?v=6",
    #     require_admin=False,
    # )

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

    return True


async def async_setup_entry(hass, entry):
    """Set up a config entry for context_provider."""
    _LOGGER.info("Setting up context_provider entry")

    # ⬇️ Intents regisztrálása
    await async_register_intents(hass)

    # ⬇️ Kontextus összeállítása (témák + metaadatok a frontmatter-ből)
    prompt_context = await build_prompt_context()

    # ⬇️ Elmentjük a prompt contextet a Home Assistant data store-ba
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["prompt_context"] = prompt_context
    hass.data[DOMAIN][entry.entry_id] = entry.data
    hass.data[DOMAIN]["google_api_key"] = entry.data.get("google_api_key")

    # ⬇️ Renderelt context Markdown exportálása (opcionális)
    await write_rendered_topics_md(prompt_context.get("topics", {}))

    # ⬇️ Platform regisztrálása (jelenleg csak sensor)
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    # ➡️ Másoljuk a context_provider_prompt.jinja fájlt induláskor
    await copy_prompt_template(hass)
    return True


async def async_unload_entry(hass, entry):
    """Unload a config entry for context_provider."""
    _LOGGER.info("Unloading context_provider entry")

    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    hass.data[DOMAIN].pop(entry.entry_id, None)

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


async def copy_prompt_template(hass):
    """Másolja a prompt Jinja sablont a Home Assistant custom_templates könyvtárába."""
    source = (
        Path(__file__).parent / "prompt_templates" / "context_provider_prompt.jinja"
    )
    target_dir = Path(hass.config.path("custom_templates"))
    target_file = target_dir / "context_provider_prompt.jinja"

    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target_file)
