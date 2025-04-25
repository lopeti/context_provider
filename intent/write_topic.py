"""Intent handler: WriteTopic"""

import os
import asyncio
import shutil
from datetime import datetime
from typing import Optional

import yaml
from homeassistant.core import HomeAssistant
from homeassistant.helpers.intent import IntentHandler

from ..helpers.intent_helpers import (
    response_with_text,
    response_error,
    normalize_topic,
    slot_or_fallback,
)

DATA_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "data", "custom")
)


class WriteTopicIntent(IntentHandler):
    """Handle writing to a topic file."""

    intent_type = "WriteTopic"

    slot_schema = {
        "topic": str,
        "content": str,
        "mode": str,  # optional: "overwrite" or "append"
    }

    async def async_handle(self, intent_obj):
        hass: HomeAssistant = intent_obj.hass
        slots = intent_obj.slots

        topic_slot = slot_or_fallback(slots, "topic")
        content = slot_or_fallback(slots, "content")
        mode = slot_or_fallback(slots, "mode") or "append"

        if not topic_slot or not content:
            return response_error(
                intent_obj, "missing_slot", "Hiányzik a téma vagy tartalom."
            )

        topic = normalize_topic(topic_slot)
        filename = os.path.join(DATA_PATH, f"{topic}.md")
        os.makedirs(DATA_PATH, exist_ok=True)

        try:
            if mode == "overwrite":
                await asyncio.get_running_loop().run_in_executor(
                    None, lambda: backup_existing_topic_file(filename)
                )
                await asyncio.get_running_loop().run_in_executor(
                    None, lambda: write_topic_with_frontmatter(filename, content, topic)
                )
            else:
                await asyncio.get_running_loop().run_in_executor(
                    None,
                    lambda: append_topic_file(filename, content),
                )

            return response_with_text(intent_obj, f"A(z) {topic} témát elmentettem.")
        except Exception as e:
            return response_error(
                intent_obj, "write_error", f"Nem sikerült menteni: {e}"
            )


def backup_existing_topic_file(path: str):
    """Save versioned backup if file already exists."""
    if not os.path.isfile(path):
        return

    history_dir = os.path.join(
        os.path.dirname(path),
        ".history",
        os.path.basename(path).replace(".md", ""),
    )
    os.makedirs(history_dir, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    backup_path = os.path.join(history_dir, f"{timestamp}.md")

    shutil.copy2(path, backup_path)


def write_topic_with_frontmatter(
    path: str, content: str, topic_name: Optional[str] = None
):
    """Write full topic file with frontmatter + content."""
    frontmatter = {
        "aliases": [],
        "label": topic_name.replace("_", " ").capitalize() if topic_name else "Unknown",
        "tags": [],
        "language": "hu",
    }

    yaml_part = yaml.dump(frontmatter, allow_unicode=True)
    full_content = f"---\n{yaml_part}---\n\n{content.strip()}\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(full_content)


def append_topic_file(path: str, content: str):
    """Append to the topic file without touching frontmatter."""
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n" + content.strip() + "\n")
