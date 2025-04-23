import yaml
from typing import Tuple


def split_frontmatter(md_content: str) -> Tuple[dict, str]:
    """Split the frontmatter and content of a Markdown file.

    Returns a tuple of (metadata, content).

    Example Markdown:
    ---
    title: Air Conditioning
    tags: [cooling, heat]
    ---
    There are two air conditioners in the house...

    """
    if md_content.startswith("---"):
        parts = md_content.split("---", 2)
        if len(parts) >= 3:
            try:
                metadata = yaml.safe_load(parts[1]) or {}
                content = parts[2].strip()
                return metadata, content
            except Exception:
                pass
    return {}, md_content.strip()
