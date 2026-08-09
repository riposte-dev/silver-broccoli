import os
import time

PATH_INPUT = "./input/"
PATH_OUTPUT = "./output/"
TEMPLATE_HTML = "./template.html"
DATE_FORMAT = "%Y.%m.%d"

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

def create_html_file(md_file):
    htmlFile = open(PATH_OUTPUT + md_file.replace(".md", ".html"), "w") # Create new or overwrite old file
    
    htmlContent = ""

    with open(TEMPLATE_HTML) as template:
        htmlContent = template.read()

    htmlContent = htmlContent.replace("[title]", file.replace(".md", ""))
    htmlContent = htmlContent.replace("[content]", find_new_lines(markdownContent))
    htmlContent = htmlContent.replace("[created]", get_file_creation_date(md_file))
    htmlContent = htmlContent.replace("[updated]", get_file_modified_date(md_file))
    
    htmlFile.write(htmlContent)

for file in os.listdir(PATH_INPUT):
    print("Parsing " + file + "...")
    
    markdownContent = ""

    with open(PATH_INPUT + file, "r") as content:
        markdownContent = content.read()

    create_html_file(file)
