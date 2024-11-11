def clean_code_block(text: str) -> str:
    """
    Removes code block markers and cleans up code block formatting.

    Args:
        text: String containing code block to clean

    Returns:
        Cleaned code block with markers removed and consistent formatting
    """
    # Handle empty input
    if not text:
        return text

    cleaned_text = text

    # Remove code block markers
    start_markers = ["```python", "```py", "```"]
    for marker in start_markers:
        if marker in cleaned_text[:200]:
            print("Found start marker")
            cleaned_text = cleaned_text[
                cleaned_text.index(marker) + len(marker) :
            ].lstrip()
            break

    end_marker = "```"
    last_800_chars = cleaned_text[-800:]
    print(f"Last 800 chars: {last_800_chars}")
    if end_marker in last_800_chars:
        print("Found end marker")
        end_index = cleaned_text.rindex(end_marker)
        cleaned_text = cleaned_text[:end_index].rstrip()

    # Clean up formatting
    lines = cleaned_text.splitlines()
    cleaned_lines = []
    for line in lines:
        # Remove excess whitespace but preserve indentation
        stripped = line.rstrip()
        if stripped:
            cleaned_lines.append(stripped)
        else:
            cleaned_lines.append("")

    # Join with newlines and add final newline
    cleaned_text = "\n".join(cleaned_lines)
    if cleaned_text:
        cleaned_text += "\n"

    return cleaned_text
