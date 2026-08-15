import math_format
import code_format

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