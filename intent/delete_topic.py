# intent/delete_topic.py

from homeassistant.helpers import intent
import os
from ..helpers.normalize_topic_filename import normalize_topic_filename


class DeleteTopicIntentHandler(intent.IntentHandler):
    """Handle deleting an entire topic (both meta and facts)."""

    intent_type = "DeleteTopic"

    async def async_handle(self, intent_obj: intent.Intent) -> intent.IntentResponse:
        hass = intent_obj.hass
        slots = intent_obj.slots

        topic_name = slots.get("topic", {}).get("value")

        if not topic_name:
            response = intent_obj.create_response()
            response.async_set_speech(
                "I could not understand the topic to delete. Please provide a topic name."
            )
            return response

        safe_topic_filename = normalize_topic_filename(topic_name)

        # Prepare paths
        base_data_dir = hass.config.path("data")
        topic_yaml_path = os.path.join(base_data_dir, f"{safe_topic_filename}.yaml")
        topic_md_path = os.path.join(base_data_dir, f"{safe_topic_filename}.md")

        # Try deleting both files
        yaml_deleted = False
        md_deleted = False

        if os.path.exists(topic_yaml_path):
            os.remove(topic_yaml_path)
            yaml_deleted = True

        if os.path.exists(topic_md_path):
            os.remove(topic_md_path)
            md_deleted = True

        # Response to user
        response = intent_obj.create_response()

        if yaml_deleted or md_deleted:
            response.async_set_speech(f"The topic '{topic_name}' has been deleted.")
        else:
            response.async_set_speech(
                f"No existing topic found for '{topic_name}'. Nothing was deleted."
            )

        return response
