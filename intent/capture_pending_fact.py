# custom_components/context_provider/intent/capture_pending_fact.py

from homeassistant.helpers import intent
from ..helpers.pending_fact_store import add_pending_fact


class CapturePendingFactIntentHandler(intent.IntentHandler):
    """Handle capturing a fact when structured CRUD is not possible."""

    intent_type = "CapturePendingFact"
    slot_schema = {
        "fact_text": str,
        "suggested_topic": str,  # Optional
    }

    async def async_handle(self, intent_obj: intent.Intent) -> intent.IntentResponse:
        hass = intent_obj.hass
        slots = intent_obj.slots

        fact_text = slots.get("fact_text", {}).get("value")
        suggested_topic = slots.get("suggested_topic", {}).get("value", None)

        if not fact_text:
            response = intent_obj.create_response()
            response.async_set_speech(
                "I could not understand the information you want to capture. Please say it again."
            )
            return response

        # Save into pending facts
        await add_pending_fact(
            hass,
            text=fact_text,
            detected_by="conversation_agent",
            detected_user="unknown",
            suggested_topic=suggested_topic,
        )

        # Confirm to the user
        response = intent_obj.create_response()
        response.async_set_speech(
            "I have saved your information for later processing. Thank you!"
        )
        return response
