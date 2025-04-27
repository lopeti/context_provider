# custom_components/context_provider/helpers/pending_fact_store.py

import yaml
import os
from datetime import datetime
from homeassistant.core import HomeAssistant
from .async_file_io import async_read_file, async_write_file

PENDING_FACTS_FILENAME = "pending_facts.yaml"


def _pending_facts_path(hass: HomeAssistant) -> str:
    """Get the full path to the pending_facts.yaml file."""
    return hass.config.path("data", PENDING_FACTS_FILENAME)


async def load_pending_facts(hass: HomeAssistant) -> list[dict]:
    """Load all pending facts from the YAML file."""
    path = _pending_facts_path(hass)
    if not os.path.exists(path):
        return []

    try:
        content = await async_read_file(path)
        data = yaml.safe_load(content)
        if not data or "pending" not in data:
            return []
        return data["pending"]
    except Exception:
        return []


async def save_pending_facts(hass: HomeAssistant, pending_facts: list[dict]) -> None:
    """Save the pending facts list back to the YAML file."""
    path = _pending_facts_path(hass)
    data = {"pending": pending_facts}
    yaml_content = yaml.dump(data, allow_unicode=True, sort_keys=False)
    await async_write_file(path, yaml_content)


async def add_pending_fact(
    hass: HomeAssistant,
    text: str,
    detected_by: str = "conversation_agent",
    detected_user: str = "unknown",
    suggested_topic: str | None = None,
) -> None:
    """Add a new pending fact entry."""
    pending_facts = await load_pending_facts(hass)

    new_entry = {
        "text": text.strip(),
        "detected_by": detected_by,
        "detected_time": datetime.utcnow().isoformat() + "Z",
        "detected_user": detected_user,
        "suggested_topic": suggested_topic,
    }

    pending_facts.append(new_entry)
    await save_pending_facts(hass, pending_facts)


async def clear_pending_facts(hass: HomeAssistant) -> None:
    """Clear all pending facts."""
    path = _pending_facts_path(hass)
    if os.path.exists(path):
        await async_write_file(path, "pending: []\n")
