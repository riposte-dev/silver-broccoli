"""
Math block environments are written
$$
equation
$$

Parse to html like so:
<div class="math-block">
$$
equation
$$
</div>

MathJaX will automatically detect "$$" delimiters and render them

In-line delimiters "$" are rendered automatically as well so no need to format them
"""

def check_for_math_delimiters(lines):
    """
    Given a list of lines from a Markdown file, return a list of indexes whose lines are "$$"
    """

    # Create a list of indexes for all math block delimiters
    math_delimiter_indexes = [] 

    # Find all "$$" delimiters
    for i in range(0, len(lines)):
        if lines[i] == "$$":
            math_delimiter_indexes.append(i)

    return math_delimiter_indexes


def check_for_math_environment(lines):
    """
    Given a list of lines from a Markdown file, return a list of indexes whose lines are in a math block environment
    """

    math_delimiter_indexes = check_for_math_delimiters(lines)
    
    # Create a list of indexes for all lines in a math block environment, including the delimiters
    math_environment_indexes = []

    # Since "$$" delimiters come in pairs, treat them as closed intervals where every index in between is also a math block environment
    for i in range(0, len(math_delimiter_indexes), 2):
        for j in range(math_delimiter_indexes[i], math_delimiter_indexes[i+1] + 1): # From 'i' to 'i+1'
            math_environment_indexes.append(j)
    
    return math_environment_indexes


def format_math_environment(lines):
    math_delimiter_indexes = check_for_math_delimiters(lines)

    if (math_delimiter_indexes == []):
        return

    # Since "$$" delimiters come in pairs, add "<div>" to the first and "</div>" to the second
    # Add opening <div> tag to first $$
    for i in range(0, len(math_delimiter_indexes), 2):
        math_delimiter_index = math_delimiter_indexes[i]
        lines[math_delimiter_index] = "<div class='math-block'>\n" + lines[math_delimiter_index]
    
    # Add closing </div> tag to second $$
    for i in range(0, len(math_delimiter_indexes), 2):
        math_delimiter_index = math_delimiter_indexes[i+1] # Add to every other index
        lines[math_delimiter_index] = lines[math_delimiter_index] + "\n</div>"

