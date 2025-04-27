import os
from .helpers.topic_loader import load_all_topic_filenames, load_topic_meta
import logging

_LOGGER = logging.getLogger(__name__)


async def build_prompt_context() -> dict:
    """Construct the dynamic prompt context using summary + keywords."""
    topics = {}
    keyword_index = {}

    topic_names = await load_all_topic_filenames()

    for topic in topic_names:
        try:
            meta = await load_topic_meta(topic)
            if not meta:
                continue

            summary = meta.get("summary", "").strip()
            keywords = [kw.strip().lower() for kw in meta.get("keywords", [])]

            topics[topic] = {
                "summary": summary,
                "keywords": keywords,
            }

            for kw in keywords:
                keyword_index.setdefault(kw, []).append(topic)
        except Exception as err:
            _LOGGER.error("Failed to process topic %s: %s", topic, err)

    # Prioritize 'about_context_provider' if present
    topics_sorted = dict(
        sorted(
            topics.items(),
            key=lambda item: (0 if item[0] == "about_context_provider" else 1, item[0]),
        )
    )

    return {
        "topics": topics_sorted,
        "keyword_index": keyword_index,
    }
