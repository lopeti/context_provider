from homeassistant.helpers import intent
from homeassistant.helpers.intent import IntentResponse
import logging

_LOGGER = logging.getLogger(__name__)

SLOT_SCHEMA_STR = {"type": "string"}  # Define a reusable slot schema for strings

def response_with_text(intent_obj, text: str) -> IntentResponse:
    response = intent_obj.create_response()
    response.async_set_speech(text)
    return response

def response_error(intent_obj, error_type: str, message: str) -> IntentResponse:
    """
    Generate an error response with a specific error type and message.
    """
    _LOGGER.error("Error response generated: type=%s, message=%s", error_type, message)
    response = intent_obj.create_response()
    response.async_set_speech(message)
    response.error_type = error_type
    return response

def normalize_topic(topic: str) -> str:
    """
    Normalize a topic by converting it to lowercase and handling aliases.
    """
    # Example alias mapping, can be extended
    aliases = {
        "Home": "home",
        "Office": "office",
    }
    return aliases.get(topic, topic.lower())

def slot_or_fallback(slots, name, default=None):
    """
    Safely read a slot's 'value' or return a default if the slot or 'value' is missing.
    """
    return slots.get(name, {}).get("value", default)