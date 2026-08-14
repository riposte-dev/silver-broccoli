"""
Code block environments are written
```lang
code
```
(where 'lang' is an optional label that users can add to specify coding language)

Parse to html like so:
<pre>
    <code class="language-lang">
        code
    </code>
</pre>

By adding a CSS class like 'language-c' to <code>, Prism.js will automatically add syntax highlighting
"""

def check_for_code_delimiters(lines):
    """
    Given a list of lines from a Markdown file, return a list of indexes whose lines contain "```"
    """

    # Create a list of indexes for all code block delimiters
    code_delimiter_indexes = []

    for i in range(0, len(lines)):
        # Users can label a language for the code block, so a valid code line may be "```" or "```language"
        if lines[i][0:3] == "```":
            code_delimiter_indexes.append(i)

    return code_delimiter_indexes


def check_for_code_environment(lines):
    """
    Given a list of lines from a Markdown file, return a list of indexes whose lines are in a code block environment
    """

    code_delimiter_indexes = check_for_code_delimiters(lines)

    # Create a list of indexes for all lines in a code block environment, including the delimiters
    code_environment_indexes = []

    # Since "```" delimiters come in pairs, treat them as closed intervals where every index in between is also a code block environment
    for i in range(0, len(code_delimiter_indexes), 2):
        for j in range(code_delimiter_indexes[i], code_delimiter_indexes[i+1] + 1): # From 'i' to 'i+1'
            code_environment_indexes.append(j)
    
    return code_environment_indexes


def format_code_environment(lines):
    code_delimiter_indexes = check_for_code_delimiters(lines)

    # Since "```" delimiters come in pairs, replace the first and second by opening and closing tags, respectively
    # Replace with opening tags
    for i in range(0, len(code_delimiter_indexes), 2):
        code_delimiter_index = code_delimiter_indexes[i]

        # No labelled coding language, wrap in code tag with no class
        if (lines[code_delimiter_index] == "```"):
            lines[code_delimiter_index] = "<pre class='code-block'>\n<code>\n"
        # There exists a labelled coding language, add class to code tag
        else:
            coding_language = lines[code_delimiter_index][3:]
            lines[code_delimiter_index] = "<pre class='code-block'>\n<code class='language-" + coding_language + "'>\n"
    
    # Replace with closing tags
    for i in range(0, len(code_delimiter_indexes), 2):
        code_delimiter_index = code_delimiter_indexes[i+1] # Add to every other index
        lines[code_delimiter_index] = "\n</code>\n</pre>"

