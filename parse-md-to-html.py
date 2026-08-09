import os # For opening, reading, and writing files
import time # For time stamps


PATH_INPUT = "./input/" # Directory for all source files in markdown
PATH_OUTPUT = "./output/" # Directory for all generated html
TEMPLATE_HTML = "./template.html"
DATE_FORMAT = "%Y.%m.%d" # Default format for get_file_creation_date() and get_file_modified_date()

def get_file_name(file):
    file_name = ""

    for i in range(len(file) - 1, 0, -1):
        # Find the last instance of "." in 'file' (i.e. "file.extension")
        if (file[i] == "."):
            file_name = file[0:i]
            break

    return file_name


def get_file_creation_date(file):
    created_seconds = os.path.getctime(PATH_INPUT + file)
    created_formatted = time.ctime(created_seconds)

    time_object = time.strptime(created_formatted)
    date = time.strftime(DATE_FORMAT, time_object)

    return date


def get_file_modified_date(file):
    modified_seconds = os.path.getmtime(PATH_INPUT + file)
    modified_formatted = time.ctime(modified_seconds)
    
    time_object = time.strptime(modified_formatted)
    date = time.strftime(DATE_FORMAT, time_object)

    return date


def find_new_lines(content):
    content_formatted = "" # Return markdown content formatted for html

    lines = content.split("\n") # Create a list of all lines in markdown content

    # Remove any empty, new lines
    while "" in lines:
        lines.remove("")
    
    math_block_indexes = [] # A list of indexes of all "$$" delimiters

    for i in range(0, len(lines)):
        if lines[i] == "$$":
            math_block_indexes.append(i)
    
    # Create a version of 'lines' that stores indexes of elements
    paragraph_indexes = [] # A list of indexes of all text paragraphs

    for i in range(0, len(lines)):
        paragraph_indexes.append(i)
    
    # Remove the indexes of any lines in a math environment
    for i in range(0, len(math_block_indexes), 2):
        for j in range(math_block_indexes[i], math_block_indexes[i+1] + 1):
            paragraph_indexes.remove(j)

    # Apply html paragraph element to remaining lines
    for i in paragraph_indexes:
        lines[i] = "<p>" + lines[i] + "</p>"
    
    # Sum the content into html format
    for line in lines:
        content_formatted += line + "\n"
    
    return content_formatted


def generate_html_file(md_file):
    # Read content from files
    markdown_content = ""
    with open(PATH_INPUT + md_file, "r") as content:
        markdown_content = content.read()

    html_content = ""
    with open(TEMPLATE_HTML) as template:
        html_content = template.read() # Copy html boilerplate from template file
    
    html_file = open(PATH_OUTPUT + md_file.replace(".md", ".html"), "w") # Create new or overwrite old file

    # Fill out placeholders
    html_content = html_content.replace("[title]", get_file_name(md_file))
    html_content = html_content.replace("[content]", find_new_lines(markdown_content))
    html_content = html_content.replace("[created]", get_file_creation_date(md_file))
    html_content = html_content.replace("[updated]", get_file_modified_date(md_file))
    
    return html_file.write(html_content) # Write the formatted content to html file


# Generate html (to ./output) for every markdown file (in ./input)
for md_file in os.listdir(PATH_INPUT):
    if (md_file.endswith(".md") == False):
        continue # Ignore any files that aren't markdown

    print("Parsing " + md_file + "...")
    generate_html_file(md_file)

