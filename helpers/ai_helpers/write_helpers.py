"""Helpers for AI-based topic writing and rewriting using Google REST API."""

from aiohttp import ClientSession
from homeassistant.core import HomeAssistant
from ..markdown_utils import split_frontmatter
from ...helpers.markdown_fix import validate_and_fix_topic_text


async def rewrite_topic_file_with_ai(
    hass: HomeAssistant, topic: str, fact: str, original: str
) -> str:
    """
    Use Google Generative Language API to rewrite a topic file based on a new fact.
    Returns the full updated Markdown content, including YAML frontmatter and facts.
    """

    # 🧠 Prompt construction
    prompt = f"""
You are a knowledge assistant managing structured Markdown topic files.

Each file starts with a **YAML frontmatter block** containing metadata (`summary` and `keywords`), followed by a **bullet-point list of factual information** in Hungarian.

Your job is to intelligently integrate a newly received fact into the topic file, ensuring:

- 🧠 Correct formatting,
- 📚 Logical topic structure,
- 🎯 Accurate representation of knowledge,
- 🔁 Consistency with existing content.

---

### 🛠️ FRONTMATTER RULES

💡 You **must always** include or create a valid frontmatter block with the following fields:

- `summary`: a one-sentence summary (in Hungarian) describing the scope of the file.
- `keywords`: a short list of important keywords (Hungarian), each on its own line.

Use expanded YAML format:
✅ GOOD:
  keywords:
    - bojler
    - melegvíz

⛔️ BAD:
  keywords: [bojler, melegvíz]

---

🧾 FACT INTEGRATION RULES
Preserve all existing valid facts unless they contradict the new one.

Remove or rephrase conflicting facts.

Append or place the new fact in a logically fitting place in the list.

Use bullet-point format, optionally with sub-bullets for structure.

🔹 Original file:
{original.strip()}

🔹 New fact:
{fact.strip()}

✅ OUTPUT
Return the full and updated Markdown content, including:

A valid and structured YAML frontmatter block

A bullet list of facts (in Hungarian)
"""

    # 🔑 Load API key from hass.data
    api_key = hass.data.get("context_provider", {}).get("google_api_key")
    if not api_key:
        raise RuntimeError("Missing Google API key for context_provider integration")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    async with ClientSession() as session:
        try:
            async with session.post(
                url,
                json={"contents": [{"parts": [{"text": prompt}]}]},
                headers={"Content-Type": "application/json"},
                timeout=30,
            ) as response:
                if response.status != 200:
                    raise RuntimeError(
                        f"API error {response.status}: {await response.text()}"
                    )

                data = await response.json()
                raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                return validate_and_fix_topic_text(raw_text)

        except Exception as e:
            raise RuntimeError(f"Failed to call Google AI: {e}") from e
