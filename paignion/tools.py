import markdown


from paignion.definitions import MD_EXTENSIONS, TERMINAL_COLORS


def markdownify(md_string):
    """Convert a Markdown string to HTML.

    :param md_string: the Markdown string
    :type md_string: str
    """
    if not md_string:
        return md_string

    # Apply the Markdown conversion along with extensions
    return markdown.markdown(md_string, extensions=MD_EXTENSIONS)


def color_message(message, color):
    """Color a message.

    :param message: the message to color
    :type message: str
    :param color: the color to use
    :type color: str (TERMINAL_COLORS dictionary in definitions.py)
    """
    if color not in TERMINAL_COLORS:
        return message

    return TERMINAL_COLORS[color].format(message)


def info(message, end="\n"):
    """Print an info message.

    :param message: the info message to print
    :type message: str
    :param end: the end character/string ('\n' by default)
    :type end: str
    """
    print(color_message(message=f"[paignion] {message}", color="yellow"), end=end)
