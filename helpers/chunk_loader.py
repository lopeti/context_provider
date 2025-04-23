"""Module for loading and resolving topics with metadata."""

import asyncio
import os
from typing import Optional

from .markdown_utils import split_frontmatter


_alias_cache: dict[str, str] | None = None


async def build_alias_index() -> dict[str, str]:
    """Build alias -> canonical topic name index from frontmatter."""
    global _alias_cache
    if _alias_cache is not None:
        return _alias_cache

    index: dict[str, str] = {}

    topic_names = await load_all_topic_filenames()

    for topic in topic_names:
        path = await search_topic_file(topic)
        if not path:
            continue

        try:
            with open(path, "r", encoding="utf-8") as f:
                full_content = f.read()

            meta, _ = split_frontmatter(full_content)
            aliases = meta.get("aliases", [])

            # Add canonical name and aliases
            index[topic.lower()] = topic
            for alias in aliases:
                index[alias.lower()] = topic
        except Exception:
            continue

    _alias_cache = index
    return index


async def resolve_topic_alias(input_topic: str) -> str:
    index = await build_alias_index()
    return index.get(input_topic.lower(), input_topic)


async def load_topic(input_topic: str) -> Optional[dict]:
    """
    Load topic content with metadata:
    - match_type: exact | alias
    - resolved_topic: canonical name
    - content: full content (minus frontmatter)
    """
    topic_key = input_topic.lower()
    alias_index = await build_alias_index()

    resolved_topic = alias_index.get(topic_key, topic_key)
    match_type = (
        "exact"
        if topic_key == resolved_topic.lower()
        else "alias"
        if topic_key in alias_index
        else "unknown"
    )

    path = await search_topic_file(resolved_topic)
    if not path:
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            full_content = f.read()

        _, content = split_frontmatter(full_content)

        return {
            "resolved_topic": resolved_topic,
            "match_type": match_type,
            "content": content,
        }
    except Exception:
        return None


async def search_topic_file(topic: str) -> Optional[str]:
    base_dir = os.path.dirname(__file__)
    folders = ["../data", "../data/custom"]
    for folder in folders:
        path = os.path.normpath(os.path.join(base_dir, folder, f"{topic}.md"))
        if os.path.isfile(path):
            return path
    return None


async def load_all_topic_filenames() -> list[str]:
    base_dir = os.path.dirname(__file__)
    folders = ["../data", "../data/custom"]
    result = set()

    for folder in folders:
        folder_path = os.path.normpath(os.path.join(base_dir, folder))
        try:
            files = await asyncio.get_running_loop().run_in_executor(
                None, lambda: os.listdir(folder_path)
            )
            for f in files:
                if f.endswith(".md"):
                    result.add(f.replace(".md", ""))
        except Exception:
            continue

    return sorted(result)


def invalidate_alias_cache():
    """Force rebuild of alias index."""
    global _alias_cache
    _alias_cache = None
