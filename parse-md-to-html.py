import os

PATH_INPUT = "./input"
PATH_OUTPUT = "./output"

def create_html_file(md_file):
    htmlTemplate = ""
    htmlFile = open(PATH_OUTPUT + "/" + md_file.replace(".md", ".html"), "w") # Create new or overwrite old file

    with open("./template.html") as template:
        htmlTemplate = template.read()
    
    # Insert markdown content into the body of the html file
    bodyIndex = htmlTemplate.find("<body>")
    htmlContent = htmlTemplate[:bodyIndex + 6] + "\n" + markdownContent + htmlTemplate[bodyIndex + 6:] # 6 is the string length of "<body>"
    
    htmlFile.write(htmlContent)

for file in os.listdir(PATH_INPUT):
    print("Parsing " + file + "...")
    
    markdownContent = ""
    with open(PATH_INPUT + "/" + file) as content:
        markdownContent = content.read()

    create_html_file(file)
