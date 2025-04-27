import re
import unicodedata


def normalize_topic_filename(name: str) -> str:
    """Normalize a topic name into a safe, filesystem-compatible filename."""
    if not name:
        return ""

    # Step 1: Unicode normalization (e.g., é → e, á → a, etc.)
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")

    # Step 2: Convert to lowercase
    name = name.lower()

    # Step 3: Replace spaces and underscores with hyphens
    name = re.sub(r"[\s_]+", "-", name)

    # Step 4: Remove all non-alphanumeric and non-hyphen characters
    name = re.sub(r"[^a-z0-9\-]", "", name)

    # Step 5: Collapse multiple hyphens into a single hyphen
    name = re.sub(r"-{2,}", "-", name).strip("-")

    return name
