markdownContent = ""
path = "./input/test.md"

with open(path) as content:
    markdownContent = content.read()

def create_html_file():
    htmlTemplate = ""
    htmlFile = open("./output/test.html", "w")

    with open("./template.html") as template:
        htmlTemplate = template.read()
    
    bodyIndex = htmlTemplate.find("<body>")
    htmlContent = htmlTemplate[:bodyIndex + 6] + "\n" + markdownContent + htmlTemplate[bodyIndex + 6:]
    
    htmlFile.write(htmlContent)

create_html_file()