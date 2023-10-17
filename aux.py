def swap_quotes(text):
    swapped_text = ""
    for char in text:
        if char == "'":
            swapped_text += '"'
        elif char == '"':
            swapped_text += "'"
        else:
            swapped_text += char
    return swapped_text