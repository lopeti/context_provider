import os

FACTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "facts"
)

TOPIC_ALIASES = {
    "bojler": "boiler",
    "fűtés": "heating",
    "klíma": "air_conditioning",
    "energia": "energy",
    "levegő": "air_quality",
}

def resolve_topic_alias(topic: str) -> str:
    return TOPIC_ALIASES.get(topic.lower(), topic.lower())

def available_topics() -> list[str]:
    """List available chunk topics (filenames without .txt)"""
    return [
        f[:-4].lower()
        for f in os.listdir(FACTS_DIR)
        if f.endswith(".txt")
    ]

def fuzzy_match_topic_name(query: str) -> str | None:
    """Fuzzy match on topic name (filename)"""
    query = query.lower()
    for topic in available_topics():
        if query in topic:
            return topic
    return None

def fuzzy_match_by_content(query: str) -> str | None:
    """Fuzzy match on chunk content if name match fails"""
    query = query.lower()
    for topic in available_topics():
        path = os.path.join(FACTS_DIR, f"{topic}.txt")
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().lower()
                if query in content:
                    return topic
        except Exception:
            continue
    return None

def load_topic(topic: str) -> dict | None:
    """
    Load a topic chunk from file.
    Returns: dict {content, match_type, resolved_topic}
    """
    original = topic
    resolved = resolve_topic_alias(topic)
    path = os.path.join(FACTS_DIR, f"{resolved}.txt")

    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return {
                    "content": f.read(),
                    "match_type": "alias" if resolved != original else "exact",
                    "resolved_topic": resolved
                }
        except Exception:
            return None

    # 🔍 1. próbáljunk fuzzy fájlnév szerint
    fuzzy = fuzzy_match_topic_name(topic)
    if fuzzy:
        return _load_as_fuzzy(fuzzy)

    # 🔍 2. próbáljunk tartalom alapján
    fuzzy = fuzzy_match_by_content(topic)
    if fuzzy:
        return _load_as_fuzzy(fuzzy)

    return None

def _load_as_fuzzy(topic: str) -> dict | None:
    path = os.path.join(FACTS_DIR, f"{topic}.txt")
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return {
                    "content": f.read(),
                    "match_type": "fuzzy",
                    "resolved_topic": topic
                }
        except Exception:
            return None
    return None
