import os
from .chunk.chunk_loader import load_topic_metadata


def build_prompt_context() -> dict:
    """Constructs the dynamic prompt context used in the base prompt."""
    metadata = load_topic_metadata()

    # Optional: rendezzük úgy, hogy a 'about_context_provider' mindig első legyen
    topics_sorted = dict(sorted(
        metadata.items(),
        key=lambda item: (0 if item[0] == "about_context_provider" else 1, item[0])
    ))

    return {
        "topics": topics_sorted
    }
