from homeassistant.helpers import intent
from ..helpers.transaction_log import append_transaction
from ..helpers.ai_helpers.prompts import VALIDATE_EDIT_FACT_PROMPT
from ..helpers.async_file_io import read_topic_facts
from ..helpers.ai_helpers.call_ai import call_ai
from datetime import datetime


class EditFactIntentHandler(intent.IntentHandler):
    """Handle editing an existing fact for a topic (transaction log only) with AI validation."""

    intent_type = "EditFact"

    async def async_handle(self, intent_obj: intent.Intent) -> intent.IntentResponse:
        hass = intent_obj.hass
        topic = intent_obj.slots.get("topic", {}).get("value")
        original_fact = intent_obj.slots.get("original_fact", {}).get("value")
        updated_fact = intent_obj.slots.get("updated_fact", {}).get("value")

        if not topic or not original_fact or not updated_fact:
            response = intent_obj.create_response()
            response.async_set_speech(
                "I could not understand the topic or the facts. Please try again."
            )
            return response

        # Load current facts from the topic
        facts = await read_topic_facts(hass, topic)

        # Prepare validation prompt
        prompt = VALIDATE_EDIT_FACT_PROMPT.format(
            facts="\n".join(facts),
            original_fact=original_fact.strip(),
            updated_fact=updated_fact.strip(),
        )

        # Call AI for validation
        ai_response = await call_ai(hass, prompt)

        if "notfound" in ai_response.lower():
            response = intent_obj.create_response()
            response.async_set_speech(
                "The original fact could not be found in the topic. Please check and try again."
            )
            return response

        # If validation passed, append transaction
        append_transaction(
            base_path=hass.config.path("data"),
            topic=topic,
            action="edit",
            fact={"original": original_fact.strip(), "updated": updated_fact.strip()},
            timestamp=datetime.utcnow().isoformat(),
        )

        response = intent_obj.create_response()
        response.async_set_speech(
            f"The fact has been updated for the topic {topic}. It will be consolidated later."
        )
        return response
