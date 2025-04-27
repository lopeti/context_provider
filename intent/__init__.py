from homeassistant.helpers.intent import IntentHandler, async_register
from .load_topic_facts import LoadTopicFactsIntentHandler
from .list_topics import ListTopicsIntent  # Import ListTopicsIntent from its module
from .write_topic import WriteTopicIntent
from .recognize_new_fact import RecognizeNewFactIntent

from .create_topic import CreateTopicIntentHandler
from .insert_fact import InsertFactIntentHandler
from .edit_fact import EditFactIntentHandler
from .delete_fact import DeleteFactIntentHandler
from .capture_pending_fact import CapturePendingFactIntentHandler
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
    async_register(hass, ListTopicsIntent())
    async_register(hass, RecognizeNewFactIntent())

    async_register(hass, CreateTopicIntentHandler())

    # fact crud intents
    async_register(hass, InsertFactIntentHandler())
    async_register(hass, LoadTopicFactsIntentHandler())
    async_register(hass, EditFactIntentHandler())
    async_register(hass, DeleteFactIntentHandler())

    async_register(hass, CapturePendingFactIntentHandler())
    _LOGGER.debug("Intents registered successfully")


async def async_setup_intents(hass):
    """Set up intents for the context_provider integration."""
    await async_register_intents(hass)
