import os
import time


PATH_INPUT = "./input/" # Directory for all source files in markdown
PATH_OUTPUT = "./output/" # Directory for all generated html
TEMPLATE_HTML = "./template.html"
DATE_FORMAT = "%Y.%m.%d" # Default format for get_file_creation_date() and get_file_modified_date()

def get_file_name(file):
    # os.path.splitext returns ["file_name", "file_extension"]
    return os.path.splitext(file)[0]


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


def format_math_environment(lines):
    """
    Math block environments are defined like so:
    $$
    equation
    $$

    Parse to html by containing it in a divider:
    <div class="math-block">
    $$
    equation
    $$
    </div>

    MathJaX will automatically detect "$$" delimiters and render them
    """

    # Create a list of indexes of all math delimiters
    math_delimiter_indexes = []

    # Find all "$$" delimiters
    for i in range(0, len(lines)):
        if lines[i] == "$$":
            math_delimiter_indexes.append(i)

    # Since "$$" delimiters come in pairs, add "<div>" to the first and "</div" to the second
    # Add opening <div> tag to first $$
    for i in range(0, len(math_delimiter_indexes), 2):
        math_delimiter_index = math_delimiter_indexes[i]
        lines[math_delimiter_index] = "<div class='math-block'>\n" + lines[math_delimiter_index]
    
    # Add closing </div> tag to second $$
    for i in range(0, len(math_delimiter_indexes), 2):
        math_delimiter_index = math_delimiter_indexes[i+1] # Add to every other index
        lines[math_delimiter_index] = lines[math_delimiter_index] + "\n</div>"
    
    # Finally, return a list of indexes of all math environment lines, including the delimiters
    math_environment_indexes = []

    # Since "$$" delimiters come in pairs, treat them as closed intervals where every index in between is also a math environment
    for i in range(0, len(math_delimiter_indexes), 2):
        for j in range(math_delimiter_indexes[i], math_delimiter_indexes[i+1] + 1): # From 'i' to 'i+1'
            math_environment_indexes.append(j)
    
    return math_environment_indexes


def format_md_content(md_content):
    html_body_content = ""

    lines = md_content.split("\n") # Create a list of all lines in markdown content

    # Remove any empty, new lines
    while "" in lines:
        lines.remove("")

    # Create a list of indexes of all lines that are plain text
    text_environment_indexes = []

    # Assume that a line is text by default
    # Otherwise, we remove the line's index from text_environment_indexes
    for i in range(0, len(lines)):
        text_environment_indexes.append(i)
    
    # Math environment
    math_environment_indexes = format_math_environment(lines)

    for i in math_environment_indexes:
        text_environment_indexes.remove(i)
    
    for i in text_environment_indexes:
        lines[i] = "<p>" + lines[i] + "</p>"
    
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
    html_content = html_content.replace("[title]", get_file_name(md_file))
    html_content = html_content.replace("[content]", format_md_content(md_content))
    html_content = html_content.replace("[created]", get_file_creation_date(md_file))
    html_content = html_content.replace("[updated]", get_file_modified_date(md_file))
    
    html_file.write(html_content) # Write the formatted content to html file


def main():
    # Generate html (to ./output) for every markdown file (in ./input)
    for md_file in os.listdir(PATH_INPUT):
        if (md_file.endswith(".md") == False):
            continue # Ignore any files that aren't markdown

        print("Parsing " + md_file + "...")
        html_file = generate_html_file(md_file)


if __name__=="__main__":
    main()