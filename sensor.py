import logging
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import STATE_UNKNOWN

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the Context Provider Topics sensor."""
    _LOGGER.debug("Setting up Context Provider Topics sensor")

    prompt_context = hass.data.get(DOMAIN, {}).get("prompt_context", {})

    async_add_entities([ContextTopicsSensor(prompt_context)], True)


class ContextTopicsSensor(Entity):
    """Sensor entity that exposes context topics and pending changes."""

    _attr_name = "Context Provider Topics"
    _attr_icon = "mdi:comment-question-outline"
    _attr_unique_id = "context_provider_topics"

    def __init__(self, prompt_context: dict):
        """Initialize the sensor with prompt context data."""
        self._topics = prompt_context.get("topics", {})
        self._state = len(self._topics) if self._topics else STATE_UNKNOWN

    @property
    def state(self):
        """Return the number of available topics."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return additional attributes of the sensor."""
        return {
            "topics": self._topics,
            "topics_count": len(self._topics),
        }
