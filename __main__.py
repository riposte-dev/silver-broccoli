import os
import time
import file_metadata
import text_format
import math_format
import code_format
import blockquote_format

PATH_INPUT = "./input/" # Directory for all source files in markdown
PATH_OUTPUT = "./output/" # Directory for all generated html
TEMPLATE_HTML = "./template.html"
DATE_FORMAT = "%Y.%m.%d" # Default format for get_file_creation_date() and get_file_modified_date()

def format_md_content(md_content):
    lines = md_content.split("\n") # Create a list of all lines in markdown content

    # Remove all empty lines
    while "" in lines:
        lines.remove("") 

    # Parse all lines by their appropriate environment
    text_format.format_text_environment(lines) # Text needs to be formatted first (See format_text_environment())
    math_format.format_math_environment(lines)
    code_format.format_code_environment(lines)
    blockquote_format.format_blockquotes(lines)

    html_body_content = ""

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