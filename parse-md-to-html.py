markdownContent = ""
path = "./input/test.md"

with open(path) as content:
    markdownContent = content.read()

print(markdownContent)

def create_html_file():
    htmlFile = open("./output/test.html", "x")

create_html_file()