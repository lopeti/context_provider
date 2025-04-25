def validate_and_fix_topic_text(text: str) -> str:
    """
    Ensures the input Markdown text has correct YAML frontmatter formatting:
    - Removes stray ```yaml or ``` code block markers (replaces with ---)
    - Ensures frontmatter starts and ends with '---'
    """
    #  replace ```yaml with ---
    # This is a workaround for the Google Generative Language API, which sometimes adds
    # ```yaml to the beginning of the text. We remove it to ensure proper YAML frontmatter.
    #  ```yaml from the beginning of the text
    if text.startswith("```yaml"):
        # replace it with ---
        text = text.replace("```yaml", "---", 1)

    # replace ``` with ---
    text = text.replace("```", "---", 1)
    return text
