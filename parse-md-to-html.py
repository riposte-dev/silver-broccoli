markdownContent = ""
path = "./input/test.md"

with open(path) as content:
    markdownContent = content.read()

def create_html_file():
    htmlTemplate = ""
    htmlFile = open("./output/test.html", "w") # Create new or overwrite old file

    with open("./template.html") as template:
        htmlTemplate = template.read()
    
    # Insert markdown content into the body of the html file
    bodyIndex = htmlTemplate.find("<body>")
    htmlContent = htmlTemplate[:bodyIndex + 6] + "\n" + markdownContent + htmlTemplate[bodyIndex + 6:] # 6 is the string length of "<body>"
    
    htmlFile.write(htmlContent)

create_html_file()