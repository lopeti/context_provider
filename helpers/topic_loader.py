"""Module for loading topic filenames and metadata."""

import asyncio
import anyio
import yaml
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
    """Return metadata from the topic's YAML file."""
    base_dir = Path(__file__).parent
    folders = [base_dir / "../data", base_dir / "../data/custom"]

    for folder in folders:
        yaml_path = (folder / f"{topic}.yaml").resolve()
        if yaml_path.exists():
            try:
                async with await anyio.open_file(yaml_path, encoding="utf-8") as f:
                    content = await f.read()
                meta = yaml.safe_load(content)
                return meta
            except Exception:
                return None

    return None


async def load_topic_summary_keywords(topic: str) -> tuple[str, list[str]] | None:
    """Return the summary and keywords from a topic frontmatter."""
    meta = await load_topic_meta(topic)
    if not meta:
        return None

    summary = meta.get("summary", "").strip()
    keywords = meta.get("keywords", [])
    return summary, keywords
