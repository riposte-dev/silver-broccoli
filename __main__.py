import os
import time
import file_metadata
import math_format
import code_format

PATH_INPUT = "./input/" # Directory for all source files in markdown
PATH_OUTPUT = "./output/" # Directory for all generated html
TEMPLATE_HTML = "./template.html"
DATE_FORMAT = "%Y.%m.%d" # Default format for get_file_creation_date() and get_file_modified_date()

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


def format_text_environment(lines, text_environment_indexes):
    for i in text_environment_indexes:
        lines[i] = format_text_line(lines[i])
        lines[i] = "<p>" + lines[i] + "</p>"

    return lines


def format_md_content(md_content):
    html_body_content = ""

    lines = md_content.split("\n") # Create a list of all lines in markdown content

    while "" in lines:
        lines.remove("") # Remove all empty lines

    # Text environment
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

    math_format.format_math_environment(lines)

    # Code block environment
    code_environment_indexes = code_format.check_for_code_environment(lines)

    for i in code_environment_indexes:
        text_environment_indexes.remove(i)
    
    code_format.format_code_environment(lines)
    
    # Treat the remaining lines as plain text
    format_text_environment(lines, text_environment_indexes)

    # Sum the content into html format
    for line in lines:
        html_body_content += line + "\n"

    return html_body_content


def generate_html_file(md_file):
    # Read content from files
    md_content = ""
    with open(PATH_INPUT + md_file, "r") as content:
        md_content = content.read()

    html_content = ""
    with open(TEMPLATE_HTML, "r") as template:
        html_content = template.read() # Copy html boilerplate from template file
    
    html_file = open(PATH_OUTPUT + md_file.replace(".md", ".html"), "w") # Create new or overwrite old file

    # Fill out placeholders
    html_content = html_content.replace("[title]", file_metadata.get_file_name(md_file))
    html_content = html_content.replace("[content]", format_md_content(md_content))
    html_content = html_content.replace("[created]", file_metadata.get_file_creation_date(md_file))
    html_content = html_content.replace("[updated]", file_metadata.get_file_modified_date(md_file))
    
    html_file.write(html_content) # Write the formatted content to html file

    return md_file.replace(".md", ".html")


def main():
    # Generate html (to ./output) for every markdown file (in ./input)
    for md_file in os.listdir(PATH_INPUT):
        if (md_file.endswith(".md") == False):
            continue # Ignore any files that aren't markdown

        print("Parsing " + md_file + "...")
        html_file = generate_html_file(md_file)


if __name__=="__main__":
    main()