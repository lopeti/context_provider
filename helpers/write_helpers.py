"""Helpers for AI-based topic writing and rewriting using Google REST API."""

from aiohttp import ClientSession
from homeassistant.core import HomeAssistant
from .markdown_utils import split_frontmatter


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

Each file starts with a **YAML frontmatter block** containing metadata (like `aliases`, `tags`, and `label`), followed by a **bullet-point list of factual information** in Hungarian.

Your job is to intelligently integrate a newly received fact into the topic file, ensuring:

- 🧠 Correct formatting,
- 📚 Logical topic structure,
- 🎯 Accurate representation of knowledge,
- 🔁 Consistency with existing content.

---

### 🛠️ FRONTMATTER RULES

💡 You **must always** include or create a valid frontmatter block with the following fields:

---
aliases:
  - alternative names (in Hungarian)
tags:
  - short categorical keywords
label: "Human-friendly title of the topic"
language: hu
---

If the file has no frontmatter, create one from scratch.

Always use expanded YAML syntax (avoid [tag1, tag2] style).

Derive aliases from known synonyms or variations of the topic name.

Derive tags from general categories or functions mentioned in the facts.

The language must be "hu" unless instructed otherwise.

Example frontmatter:

---
aliases:
  - bojler
  - vízmelegítő
tags:
  - melegvíz
  - fűtés
label: "Bojler működése"
language: hu
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
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()

        except Exception as e:
            raise RuntimeError(f"Failed to call Google AI: {e}") from e
