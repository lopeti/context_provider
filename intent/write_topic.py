"""Intent handler: WriteTopic"""

import os
import asyncio
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

        # Ensure directory exists
        os.makedirs(DATA_PATH, exist_ok=True)

        if mode == "overwrite":
            write_mode = "w"
        else:
            write_mode = "a"

        try:
            await asyncio.get_running_loop().run_in_executor(
                None,
                lambda: open(filename, write_mode, encoding="utf-8").write(
                    content + "\n"
                ),
            )
            return response_with_text(intent_obj, f"A(z) {topic} témát elmentettem.")
        except Exception as e:
            return response_error(
                intent_obj, "write_error", f"Nem sikerült menteni: {e}"
            )
