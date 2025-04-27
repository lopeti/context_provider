# custom_components/context_provider/intent/create_topic.py

from homeassistant.helpers import intent
from ..helpers.async_file_io import async_write_file
from ..helpers.normalize_topic_filename import normalize_topic_filename
import yaml
import os


class CreateTopicIntentHandler(intent.IntentHandler):
    """Handle creating a new topic (meta + facts) from user input."""

    intent_type = "CreateTopic"

    async def async_handle(self, intent_obj: intent.Intent) -> intent.IntentResponse:
        hass = intent_obj.hass
        slots = intent_obj.slots

        topic_name = slots.get("topic", {}).get("value")
        summary = slots.get("summary", {}).get("value")
        keywords_value = slots.get("keywords", {}).get("value")

        # Normalize keywords to a list
        if isinstance(keywords_value, str):
            keywords_list = [kw.strip() for kw in keywords_value.split(",")]
        elif isinstance(keywords_value, list):
            keywords_list = [kw.strip() for kw in keywords_value]
        else:
            keywords_list = []

        if not topic_name or not summary or not keywords_list:
            response = intent_obj.create_response()
            response.async_set_speech(
                "I could not understand the topic details. Please provide a topic name, summary, and keywords."
            )
            return response

        safe_topic_filename = normalize_topic_filename(topic_name)

        # Prepare file paths
        base_data_dir = hass.config.path("data")
        topic_yaml_path = os.path.join(base_data_dir, f"{safe_topic_filename}.yaml")
        topic_md_path = os.path.join(base_data_dir, f"{safe_topic_filename}.md")

        # Check if topic already exists (to avoid overwriting)
        if os.path.exists(topic_yaml_path) or os.path.exists(topic_md_path):
            response = intent_obj.create_response()
            response.async_set_speech(
                f"A topic named '{topic_name}' already exists. Please choose a different name."
            )
            return response

        # Prepare metadata
        metadata = {
            "summary": summary.strip(),
            "keywords": keywords_list,
            "parent_topic": None,
            "related_topics": [],
        }

        # Write metadata YAML
        yaml_content = yaml.dump(metadata, allow_unicode=True, sort_keys=False)
        await async_write_file(topic_yaml_path, yaml_content)

        # Write empty facts file
        await async_write_file(topic_md_path, "- ")

        # Respond to the user
        response = intent_obj.create_response()
        response.async_set_speech(
            f"The new topic '{topic_name}' has been created successfully. You can now add facts to it."
        )
        return response
