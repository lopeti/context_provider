from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import STATE_UNKNOWN
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the context provider sensor platform."""
    prompt_context = hass.data[DOMAIN].get("prompt_context", {})
    async_add_entities([ContextTopicsSensor(prompt_context)], True)


class ContextTopicsSensor(Entity):
    """Sensor that exposes the available ProvideTopicFacts topics."""

    _attr_name = "Context Provider Topics"
    _attr_icon = "mdi:comment-question-outline"
    _attr_unique_id = "context_provider_topics"

    def __init__(self, prompt_context: dict):
        self._topics = prompt_context.get("topics", {})
        self._state = len(self._topics) if self._topics else STATE_UNKNOWN

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {
            "topics": self._topics,
            "topics_count": len(self._topics),
        }

    async def async_update(self):
        """Update not implemented — sensor is static unless reloaded."""
        pass
