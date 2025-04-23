from homeassistant.helpers.intent import IntentHandler, async_register
from .provide_topic_facts import ProvideTopicFactsIntent

import logging

_LOGGER = logging.getLogger(__name__)


class DummyIntent(IntentHandler):
    intent_type = "DummyContextIntent"

    async def async_handle(self, intent_obj):
        response = intent_obj.create_response()
        response.async_set_speech("A context_provider működik!")
        _LOGGER.debug("Handling intent: %s", intent_obj.intent_name)
        return response


async def async_register_intents(hass):
    _LOGGER.debug("Registering intents")
    # async_register(hass, DummyIntent())
    async_register(hass, ProvideTopicFactsIntent())


async def async_setup_intents(hass):
    """Set up intents for the context_provider integration."""
    await async_register_intents(hass)
