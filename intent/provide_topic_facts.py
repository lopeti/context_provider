# Home Assistant intent handler: ProvideTopicFacts
# Slot: topic (e.g. "energy", "boiler", "air_quality")
# Loads the contents of facts/<topic>.txt and returns it as speech
# Uses alias and fuzzy match if needed, and returns context-aware message

import os
from homeassistant.helpers.intent import IntentHandler
from homeassistant.core import HomeAssistant
from ..const import DOMAIN
from ..chunk.chunk_loader import load_topic  # Advanced loader with match info
from ..helpers.intent_helpers import (
    SLOT_SCHEMA_STR,
    response_with_text,
    response_error,
    normalize_topic,
    slot_or_fallback,
)


class ProvideTopicFactsIntent(IntentHandler):
    intent_type = "ProvideTopicFacts"
    slot_schema = {"topic": SLOT_SCHEMA_STR}

    async def async_handle(self, intent_obj):
        hass: HomeAssistant = intent_obj.hass
        slots = intent_obj.slots

        topic_slot = slot_or_fallback(slots, "topic")
        if not topic_slot:
            return response_error(intent_obj, "missing_slot", "Nem adtál meg témát.")

        topic = normalize_topic(topic_slot)

        result = await load_topic(topic)
        if result is None:
            return response_error(
                intent_obj, "not_found", f"Nincs tudásom a(z) {topic_slot} témáról."
            )

        content = result["content"]
        match_type = result["match_type"]
        resolved = result["resolved_topic"]

        # 🧠 Kontextusfüggő válasz
        if match_type == "fuzzy":
            return response_with_text(
                intent_obj,
                f"A témát a „{resolved}” fájl alapján töltöttem be, mert hasonlónak tűnt. {content}",
            )
        elif match_type == "alias":
            return response_with_text(
                intent_obj,
                f"A(z) „{topic_slot}” ismert alias a „{resolved}” témához. {content}",
            )
        else:
            return response_with_text(intent_obj, content)
