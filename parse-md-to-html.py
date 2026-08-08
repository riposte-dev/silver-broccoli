import os

PATH_INPUT = "./input"
PATH_OUTPUT = "./output"

def create_html_file(md_file):
    htmlFile = open(PATH_OUTPUT + "/" + md_file.replace(".md", ".html"), "w") # Create new or overwrite old file
    
    htmlContent = ""

    with open("./template.html") as template:
        htmlContent = template.read()
    
    htmlContent = htmlContent.replace("[title]", file.replace(".md", ""))
    htmlContent = htmlContent.replace("[content]", markdownContent)
    
    htmlFile.write(htmlContent)

for file in os.listdir(PATH_INPUT):
    print("Parsing " + file + "...")
    
    markdownContent = ""

    with open(PATH_INPUT + "/" + file, "r") as content:
        markdownContent = content.read()

    create_html_file(file)
