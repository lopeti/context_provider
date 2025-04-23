import os
import yaml

_cached_aliases = None


def load_topic_metadata() -> dict:
    """Load built-in + custom topic aliases and merge them."""
    global _cached_aliases
    if _cached_aliases is not None:
        return _cached_aliases

    base_path = os.path.join(os.path.dirname(__file__), "..", "data", "topics.yaml")
    custom_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "custom/topics.yaml"
    )

    base = {}
    custom = {}

    try:
        with open(base_path, "r", encoding="utf-8") as f:
            base = yaml.safe_load(f) or {}
    except Exception:
        pass

    try:
        with open(custom_path, "r", encoding="utf-8") as f:
            custom = yaml.safe_load(f) or {}
    except Exception:
        pass

    merged = {**base, **custom}
    _cached_aliases = merged
    return merged


def resolve_topic_alias(input_topic: str) -> str:
    input_topic = input_topic.lower()
    metadata = load_topic_metadata()

    if input_topic in metadata:
        return input_topic

    for canonical, info in metadata.items():
        aliases = info.get("aliases", [])
        if input_topic in [a.lower() for a in aliases]:
            return canonical

    return input_topic


def search_topic_file(topic: str) -> str | None:
    """Search for the topic in the data folders."""
    base_dir = os.path.dirname(__file__)
    folders = ["../data", "../data/custom"]
    for folder in folders:
        file_path = os.path.join(base_dir, folder, f"{topic}.md")
        if os.path.isfile(file_path):
            return file_path
    return None


def load_topic(input_topic: str) -> dict | None:
    """
    Load topic content with metadata:
    - match_type: exact | alias
    - resolved_topic: canonical name
    - content: file content
    """
    input_topic = input_topic.lower()
    resolved_topic = resolve_topic_alias(input_topic)
    match_type = "exact" if input_topic == resolved_topic else "alias"

    file_path = search_topic_file(resolved_topic)
    if not file_path:
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return {
            "resolved_topic": resolved_topic,
            "match_type": match_type,
            "content": content,
        }
    except Exception:
        return None
