import math_format
import code_format

def find_matches(delimiter, string):
    first_index = string.find(delimiter)

    if (first_index == -1):
        return []
        
    second_index = string.find(delimiter, first_index + 1)

    if (second_index == -1):
        return []

    # Check if the special character is in inline $math$
    dollar_sign_count = 0

    for i in range(second_index, -1, -1):
        if (string[i] != "$"):
            continue

        dollar_sign_count += 1

    if (dollar_sign_count % 2 == 1):
        return []

    backtick_count = 0

    delimiter_length = len(delimiter)
    match = string[first_index:second_index + delimiter_length]

    return [match] + find_matches(delimiter, string[second_index + delimiter_length:])


def format_text_line(line):
    # Check for bolded
    bolded = find_matches("**", line) # Any text of the form: **text**

    for match in bolded:
        line = line.replace(match, "<strong>" + match[2:-2] + "</strong>") # Replace **'s with html tags

    # Check for italicized
    italicized = find_matches("*", line) + find_matches("_", line) # Italics denoted by *text* or _text_

    for match in italicized:
        line = line.replace(match, "<em>" + match[1:-1] + "</em>") # Replace * or _ with html tags

    # Check for inline code
    inline_code = find_matches("`", line) # Any text of the form: `text`

    for match in inline_code:
        line = line.replace(match, "<code>" + match[1:-1] + "</code>") # Replace ` with html tags
    
    return line


def check_for_text_environment(lines):
    # Create a list of indexes of all lines that are plain text
    text_environment_indexes = []

    # Assume that a line is text by default
    # Otherwise, we remove the line's index from text_environment_indexes
    for i in range(0, len(lines)):
        text_environment_indexes.append(i)
    
    # Math block environment
    math_environment_indexes = math_format.check_for_math_environment(lines)

    for i in math_environment_indexes:
        text_environment_indexes.remove(i)

    # Code block environment
    code_environment_indexes = code_format.check_for_code_environment(lines)

    for i in code_environment_indexes:
        text_environment_indexes.remove(i)
    
    return text_environment_indexes


def format_text_environment(lines):
    text_environment_indexes = check_for_text_environment(lines)

    for i in text_environment_indexes:
        lines[i] = format_text_line(lines[i])
        lines[i] = "<p>" + lines[i] + "</p>"

    return lines

