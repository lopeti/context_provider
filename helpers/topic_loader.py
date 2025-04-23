"""Module for loading topic filenames and metadata."""

import asyncio
import anyio
from pathlib import Path

from .chunk_loader import search_topic_file
from .markdown_utils import split_frontmatter


async def load_all_topic_filenames() -> list[str]:
    """Return a list of all topic file names (without extension)."""
    base_dir = Path(__file__).parent
    folders = [base_dir / "../data", base_dir / "../data/custom"]
    result = set()

    for folder in folders:
        try:
            files = await asyncio.get_running_loop().run_in_executor(
                None, lambda folder=folder: list(folder.iterdir())
            )
            for file in files:
                if file.suffix == ".md":
                    result.add(file.stem)  # Strip ".md"
        except FileNotFoundError:
            continue

    return sorted(result)


async def load_topic_meta(topic: str) -> dict | None:
    """Return frontmatter metadata only for the given topic."""
    path = await search_topic_file(topic)
    if not path:
        return None

    try:
        async with await anyio.open_file(path, encoding="utf-8") as f:
            content = await f.read()
        meta, _ = split_frontmatter(content)
    except FileNotFoundError:
        return None
    else:
        return meta
