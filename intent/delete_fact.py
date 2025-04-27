from homeassistant.helpers import intent
from ..helpers.transaction_log import append_transaction
from ..helpers.ai_helpers.prompts import VALIDATE_DELETE_FACT_PROMPT
from ..helpers.async_file_io import read_topic_facts
from ..helpers.ai_helpers.call_ai import call_ai
from datetime import datetime


class DeleteFactIntentHandler(intent.IntentHandler):
    """Handle deleting a fact from a topic (transaction log only) with AI validation."""

    intent_type = "DeleteFact"

    async def async_handle(self, intent_obj: intent.Intent) -> intent.IntentResponse:
        hass = intent_obj.hass
        topic = intent_obj.slots.get("topic", {}).get("value")
        fact = intent_obj.slots.get("fact", {}).get("value")

        if not topic or not fact:
            response = intent_obj.create_response()
            response.async_set_speech(
                "I could not understand the topic or the fact to delete. Please try again."
            )
            return response

        # Load current facts from the topic
        facts = await read_topic_facts(hass, topic)

        # Prepare validation prompt
        prompt = VALIDATE_DELETE_FACT_PROMPT.format(
            facts="\n".join(facts), fact_to_delete=fact.strip()
        )

        # Call AI for validation
        ai_response = await call_ai(hass, prompt)

        if "notfound" in ai_response.lower():
            response = intent_obj.create_response()
            response.async_set_speech(
                "The fact to delete could not be found in the topic. Please check and try again."
            )
            return response

        # If validation passed, append transaction
        append_transaction(
            base_path=hass.config.path("data"),
            topic=topic,
            action="delete",
            fact=fact.strip(),
            timestamp=datetime.utcnow().isoformat(),
        )

        response = intent_obj.create_response()
        response.async_set_speech(
            f"The fact has been removed from the topic {topic}. It will be consolidated later."
        )
        return response
