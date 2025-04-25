"""Intent handler: RecognizeNewFact"""

import asyncio
from homeassistant.core import HomeAssistant
from homeassistant.helpers.intent import IntentHandler

from ..prompt_builder import build_prompt_context

from ..helpers.intent_helpers import (
    response_with_text,
    response_error,
    slot_or_fallback,
    normalize_topic,
)

from ..helpers.chunk_loader import load_topic, search_topic_file
from ..helpers.ai_helpers.write_helpers import rewrite_topic_file_with_ai
from ..helpers.fs_helpers import safe_write_topic_file


class RecognizeNewFactIntent(IntentHandler):
    """Handle recognition of a new fact and update the related topic."""

    intent_type = "RecognizeNewFact"

    slot_schema = {
        "topic": str,
        "fact": str,
    }

    async def async_handle(self, intent_obj):
        hass: HomeAssistant = intent_obj.hass
        slots = intent_obj.slots

        topic = slot_or_fallback(slots, "topic")
        fact = slot_or_fallback(slots, "fact")

        if not topic or not fact:
            return response_error(
                intent_obj, "missing_slot", "Missing required slot: topic or fact."
            )

        topic = normalize_topic(topic)

        # Load existing content if available
        topic_data = await load_topic(topic)
        existin_metadata = topic_data["metadata"] if topic_data else ""
        existing_content = topic_data["content"] if topic_data else ""
        existing_raw_content = f"{existin_metadata}\n{existing_content}".strip()

        try:
            updated = await rewrite_topic_file_with_ai(
                hass=hass,
                topic=topic,
                fact=fact,
                original=existing_raw_content,
            )
        except Exception as e:
            return response_error(
                intent_obj, "ai_error", f"AI-based update failed: {e}"
            )

        path = await search_topic_file(topic)
        if not path:
            path = f"{hass.config.path('custom_components/context_provider/data/custom')}/{topic}.md"

        try:
            if updated.startswith("```markdown"):
                updated = updated.removeprefix("```markdown").strip()
                if updated.endswith("```"):
                    updated = updated.removesuffix("```").strip()
            safe_write_topic_file(path, updated)

            # refresh prompt context
            prompt_context = await build_prompt_context()
            hass.data["context_provider"]["prompt_context"] = prompt_context
            return response_with_text(
                intent_obj, f"Topic '{topic}' was successfully updated."
            )
        except Exception as e:
            return response_error(
                intent_obj, "write_error", f"Failed to save topic file: {e}"
            )
