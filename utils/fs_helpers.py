import os

def safe_write_topic_file(file_path: str, content: str):
    """Safely writes the topic content to the specified file."""
    if ".." in os.path.normpath(file_path):
        raise ValueError("Illegal file name")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)