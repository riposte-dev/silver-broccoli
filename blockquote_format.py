"""
Block quotes are written
> Quote
> Attribution
Block quotes may be single or multiline

Parse to html like so:
<blockquote>
    <p>Quote</p>
    <p>Attribution</p>
</blockquote>

Unlike math_format and code_format, we don't need to look separately for delimiters and environments

However, we do need to use the text_format module to format text within the blockquote
"""
import text_format

def check_for_blockquotes(lines):
    blockquote_indexes = []

    for line in lines:
        if (line[:2] == "> "):
            blockquote_indexes.append(lines.index(line))
    
    return blockquote_indexes


def sort_blockquote_indexes(blockquote_indexes):
    """
    Sort blockquote_indexes into continuous intervals
    e.g. [1, 3, 4, 5, 9, 10] => [[1], [3, 4, 5], [9, 10]]
    """

    blockquote_intervals = []

    interval = [blockquote_indexes[0]]

    for i in range(1, len(blockquote_indexes), 1):
        if (blockquote_indexes[i] == blockquote_indexes[i-1] + 1):
            interval.append(blockquote_indexes[i])
        else:
            blockquote_intervals.append(interval)
            interval = []
            interval.append(blockquote_indexes[i])
        
    blockquote_intervals.append(interval)

    return blockquote_intervals


def format_blockquotes(lines):
    blockquote_indexes = check_for_blockquotes(lines)

    # Format text in lines contained inside blockquote
    for i in blockquote_indexes:
        line = text_format.format_text_line(lines[i])
        lines[i] = "<p>" + line[2:] + "</p>"
    
    blockquote_intervals = sort_blockquote_indexes(blockquote_indexes)

    # For each continuous interval, add an opening and closing tag to the first and last index, respectively
    for interval in blockquote_intervals:
        for i in interval:
            # If i is the first index of interval, add an opening tag
            if (i == interval[0]):
                lines[i] = "<blockquote>" + lines[i]
            
            # If i is the last index of interval, add a closing tag
            if (i == interval[len(interval) - 1]):
                lines[i] = lines[i] + "</blockquote>"

