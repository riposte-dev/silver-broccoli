import os
import time

PATH_INPUT = "./input"
PATH_OUTPUT = "./output"

def get_file_creation_date(file):
    created_seconds = os.path.getctime(PATH_INPUT + "/" + file)
    created_formatted = time.ctime(created_seconds)

    time_object = time.strptime(created_formatted)
    date = time.strftime("%Y %m %d", time_object)

    return date

def get_file_modified_date(file):
    modified_seconds = os.path.getmtime(PATH_INPUT + "/" + file)
    modified_formatted = time.ctime(modified_seconds)
    
    time_object = time.strptime(modified_formatted)
    date = time.strftime("%Y %m %d", time_object)

    return date

def create_html_file(md_file):
    htmlFile = open(PATH_OUTPUT + "/" + md_file.replace(".md", ".html"), "w") # Create new or overwrite old file
    
    htmlContent = ""

    with open("./template.html") as template:
        htmlContent = template.read()
    
    htmlContent = htmlContent.replace("[title]", file.replace(".md", ""))
    htmlContent = htmlContent.replace("[content]", markdownContent)
    htmlContent = htmlContent.replace("[created]", get_file_creation_date(md_file))
    htmlContent = htmlContent.replace("[updated]", get_file_modified_date(md_file))
    
    htmlFile.write(htmlContent)

for file in os.listdir(PATH_INPUT):
    print("Parsing " + file + "...")
    
    markdownContent = ""

    with open(PATH_INPUT + "/" + file, "r") as content:
        markdownContent = content.read()

    create_html_file(file)
