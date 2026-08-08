markdownContent = ""
path = "./input/test.md"

with open(path) as content:
    markdownContent = content.read()

print(markdownContent)