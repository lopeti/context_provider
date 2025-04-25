"""Helpers for intent handling in the context_provider integration."""

from homeassistant.helpers.intent import IntentResponse
import logging
import re

_LOGGER = logging.getLogger(__name__)

SLOT_SCHEMA_STR = {"type": "string"}  # Define a reusable slot schema for strings


def response_with_text(intent_obj, text: str) -> IntentResponse:
    """Return a response with the provided text."""
    response = intent_obj.create_response()
    response.async_set_speech(text)
    return response


def response_error(intent_obj, error_type: str, message: str) -> IntentResponse:
    """Generate an error response with a specific error type and message."""
    _LOGGER.error("Error response generated: type=%s, message=%s", error_type, message)
    response = intent_obj.create_response()
    response.async_set_speech(message)
    response.error_type = error_type
    return response


def slot_or_fallback(slots, name, default=None):
    """Safely read a slot's 'value' or return a default if the slot or 'value' is missing.

    Handles both string and dict-based slot formats.
    """
    slot = slots.get(name)
    if isinstance(slot, dict) and "value" in slot:
        return slot["value"]
    if isinstance(slot, str):
        return slot

    _LOGGER.warning("slot_or_fallback: Unexpected slot format for '%s': %s", name, slot)
    return default


def normalize_topic(text: str | dict) -> str:
    """
    Convert a topic slot (string or slot dict) to a normalized slug identifier.
    """
    if isinstance(text, dict):
        _LOGGER.warning(
            "normalize_topic: Received a dictionary, extracting 'value' if present: %s",
            text,
        )
        text = text.get("value", "")

    if not isinstance(text, str):
        _LOGGER.error(
            "normalize_topic: Input is not a string even after extraction: %s", text
        )
        return ""

    return re.sub(r"[^\w]+", "_", text.strip().lower()).strip("_")
