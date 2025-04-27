# custom_components/context_provider/helpers/async_file_io.py
import os
import asyncio
from typing import Optional


async def read_topic_facts(hass, topic: str) -> list[str]:
    """Reads only the facts (bullet points) from the topic's .md file."""
    path = await search_topic_file(topic)
    if not path:
        raise FileNotFoundError(f"Topic file not found for topic: {topic}")

    content = await async_read_file(path)

    facts = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            facts.append(stripped[2:].strip())

    return facts


async def async_read_file(path: str) -> str:
    """Reads file content asynchronously using executor."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None, lambda: open(path, "r", encoding="utf-8").read()
    )


async def async_write_file(path: str, content: str) -> None:
    """Writes content to file asynchronously using executor."""
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(
        None, lambda: open(path, "w", encoding="utf-8").write(content)
    )


async def async_append_file(path: str, content: str) -> None:
    """Appends content to file asynchronously using executor."""
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(
        None, lambda: open(path, "a", encoding="utf-8").write(content)
    )


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
