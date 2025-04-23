"""Home Assistant intent handler: ListTopics"""

from homeassistant.helpers.intent import IntentHandler
from homeassistant.core import HomeAssistant
from ..helpers.intent_helpers import response_with_text
from ..chunk.chunk_loader import load_all_topic_filenames  # Ezt külön írd meg


class ListTopicsIntent(IntentHandler):
    """Intent handler to list all available topics."""

    intent_type = "ListTopics"

    async def async_handle(self, intent_obj):
        hass: HomeAssistant = intent_obj.hass

        # Töltsük be az összes elérhető fájl nevét (pl. heating.md, energy.md)
        topics = await load_all_topic_filenames()

        if not topics:
            return response_with_text(intent_obj, "Nem található egyetlen téma sem.")

        topic_list = ", ".join(topics)
        return response_with_text(intent_obj, f"Az elérhető témák: {topic_list}")
