# context_provider/helpers/ai_helpers/prompts.py

VALIDATE_INSERT_FACT_PROMPT = """
You are a knowledge base assistant.

Here is the current list of facts:

{facts}

A user wants to add the following new fact:

{new_fact}

✅ Your task:
- Check if the new fact already exists (exact or similar form).
- Check if the new fact conflicts with any existing fact.
- If it is a duplicate or conflict, reply clearly: "Duplicate" or "Conflict".
- If the new fact is acceptable, reply: "OK".

⚠️ Only reply with one word: "OK", "Duplicate", or "Conflict".
"""
VALIDATE_EDIT_FACT_PROMPT = """
You are a knowledge base assistant.

Here is the current list of facts:

{facts}

A user wants to edit the following fact:

Original fact: {original_fact}
Updated fact: {updated_fact}

✅ Your task:
- Check if the original fact exists in the current facts.
- If it does, reply "OK".
- If it does not exist, reply "NotFound".

⚠️ Only reply with one word: "OK" or "NotFound".
"""

VALIDATE_DELETE_FACT_PROMPT = """
You are a knowledge base assistant.

Here is the current list of facts:

{facts}

A user wants to delete the following fact:

{fact_to_delete}

✅ Your task:
- Check if the fact to delete exists in the current facts.
- If it does, reply "OK".
- If it does not exist, reply "NotFound".

⚠️ Only reply with one word: "OK" or "NotFound".
"""


REWRITE_TOPIC_FILE_PROMPT = """\
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
{original}

🔹 New fact:
{fact}

✅ OUTPUT
Return the full and updated Markdown content, including:

A valid and structured YAML frontmatter block

A bullet list of facts (in Hungarian)
"""
