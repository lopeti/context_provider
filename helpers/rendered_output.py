import os
import asyncio


def render_topics_markdown(topics: dict) -> str:
    """Render the topic list as a markdown document."""
    lines = ["### 📚 Available Topics\n"]
    for topic, info in topics.items():
        summary = info.get("summary", "No summary available.")
        keywords = info.get("keywords", [])
        keywords_str = ", ".join(keywords) if keywords else "–"
        lines.append(f"- **{topic}**: {summary}\n  _Keywords: {keywords_str}_")
    return "\n".join(lines)


async def write_rendered_topics_md(topics: dict, output_path: str | None = None):
    """Write the rendered markdown to a file."""
    if output_path is None:
        base_dir = os.path.dirname(__file__)
        output_path = os.path.join(base_dir, "..", "rendered_topics.md")

    markdown = render_topics_markdown(topics)

    try:
        await asyncio.get_running_loop().run_in_executor(
            None, lambda: open(output_path, "w", encoding="utf-8").write(markdown)
        )
    except Exception as e:
        # Silent fail for production
        print(f"⚠️ Could not write rendered_topics.md: {e}")
