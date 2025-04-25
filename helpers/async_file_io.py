# custom_components/context_provider/helpers/async_file_io.py

import asyncio


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
