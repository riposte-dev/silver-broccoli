markdownContent = ""
path = "./input/test.md"

with open(path) as content:
    markdownContent = content.read()

def create_html_file():
    htmlTemplate = ""
    htmlFile = open("./output/test.html", "x")

    with open("./template.html") as template:
        htmlTemplate = template.read()
    
    htmlFile.write(htmlTemplate)

create_html_file()