"""Module for loading and resolving topics with metadata (summary + keywords only)."""

import asyncio
import os
from typing import Optional

from .markdown_utils import split_frontmatter
from .async_file_io import async_read_file

_keyword_cache: dict[str, str] | None = None


async def build_keyword_index() -> dict[str, str]:
    """Build keyword -> canonical topic name index from frontmatter."""
    global _keyword_cache
    if _keyword_cache is not None:
        return _keyword_cache

    index: dict[str, str] = {}
    topic_names = await load_all_topic_filenames()

    for topic in topic_names:
        path = await search_topic_file(topic)
        if not path:
            continue

        try:
            full_content = await async_read_file(path)
            meta, _ = split_frontmatter(full_content)
            keywords = meta.get("keywords", [])
            for keyword in keywords:
                index[keyword.strip().lower()] = topic
        except Exception:
            continue

    _keyword_cache = index
    return index


async def resolve_topic_by_keyword(input_term: str) -> Optional[str]:
    """Try to resolve a topic name by keyword matching."""
    index = await build_keyword_index()
    return index.get(input_term.strip().lower())


async def load_topic(input_topic: str) -> Optional[dict]:
    """
    Load topic content with metadata:
    - match_type: exact | keyword | unknown
    - resolved_topic: canonical name
    - metadata: frontmatter metadata
    - content: full content (minus frontmatter)
    """
    topic_key = input_topic.strip().lower()
    topic_names = await load_all_topic_filenames()

    if topic_key in [t.lower() for t in topic_names]:
        resolved_topic = topic_key
        match_type = "exact"
    else:
        resolved_topic = await resolve_topic_by_keyword(topic_key)
        match_type = "keyword" if resolved_topic else "unknown"

    if not resolved_topic:
        return None

    path = await search_topic_file(resolved_topic)
    if not path:
        return None

    try:
        full_content = await async_read_file(path)
        metadata, content = split_frontmatter(full_content)

        return {
            "resolved_topic": resolved_topic,
            "match_type": match_type,
            "metadata": metadata,
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


def invalidate_keyword_cache():
    """Force rebuild of keyword index."""
    global _keyword_cache
    _keyword_cache = None
