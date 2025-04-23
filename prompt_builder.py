"""Helper functions for building dynamic prompt contexts."""

from .helpers.topic_loader import load_all_topic_filenames, load_topic_meta


async def build_prompt_context() -> dict:
    """Construct the dynamic prompt context using frontmatter metadata."""
    topics = {}
    topic_names = await load_all_topic_filenames()

    for topic in topic_names:
        meta = await load_topic_meta(topic)
        if meta:
            topics[topic] = meta

    # Optionally prioritize 'about_context_provider'
    topics_sorted = dict(
        sorted(
            topics.items(),
            key=lambda item: (0 if item[0] == "about_context_provider" else 1, item[0]),
        )
    )

    return {"topics": topics_sorted}
