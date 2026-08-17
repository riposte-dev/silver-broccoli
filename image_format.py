"""
Images in Markdown are written
![alt text](path to file)

Parse to html like so:
<img alt="alt text" src="path to file">

For now, assume that any image is embedded on its own new line
"""

SYMBOLS = ["[", "](", ")"]

def check_for_image(string):
    symbol_indexes = []

    for symbol in SYMBOLS:
        if (symbol_indexes == []):
            first_index = string.find(SYMBOLS[0])
            symbol_indexes.append(first_index)
        else:
            previous_index = symbol_indexes[-1]
            next_index = string.find(symbol, previous_index + 1) # Start search from previous index
            symbol_indexes.append(next_index)
    
    for index in symbol_indexes:
        if (index == -1):
            return 
    
    first_index = symbol_indexes[0]
    second_index = symbol_indexes[1]
    third_index = symbol_indexes[2]

    alt_text = string[first_index + 1:second_index]
    path_to_image = string[second_index + 2: third_index]

    return [alt_text, path_to_image]

def format_image(lines):
    for line in lines:
        image = check_for_image(line)

        if (image == None):
            continue

        alt_text = image[0]
        path_to_image = "../" + image[1]

        index = lines.index(line)

        lines[index] = "<img alt='" + alt_text + "' src='" + path_to_image + "'>"
        print(lines[index])


format_image("![alt text](path)")
format_image("This is an image ![alt text](path)")