import markdown


from paignion.definitions import MD_EXTENSIONS, TERMINAL_COLORS


def markdownify(string):
    if not string:
        return string

    return markdown.markdown(string, extensions=MD_EXTENSIONS)


def color_message(message, color, end="\n"):
    """Color a message.

    :param message:  The message to print.
    :type message:  string
    :param color:    The color to print in.
    :type color:    string (TERMINAL_COLORS dictionary in definitions.py)
    :param end:      The end character/string ('\n' by default)
    :type end:      string
    """
    if color not in TERMINAL_COLORS:
        return
    else:
        return TERMINAL_COLORS[color].format(message)


def info(message, end="\n"):
    """Print an info message.

    :param message:  The message to print.
    :type message:  string
    :param end:      The end character/string ('\n' by default)
    :type end:      string
    """
    print(color_message(message=f"[paignion] {message}", color="yellow"), end=end)


def warn(message, end="\n"):
    """Print a warning message.

    :param message:  The message to print.
    :type message:  string
    :param end:      The end character/string ('\n' by default)
    :type end:      string
    """
    print(color_message(message=f"[paignion] /!\\ {message}", color="orange"), end=end)


def fail(message, end="\n"):
    """Print a fail message, cleans up and exits.

    :param message:  The message to print.
    :type message:  string
    :param message:  A list of files to clean up.
    :type message:  list
    :param end:      The end character/string ('\n' by default)
    :type       end:      string
    """
    print(color_message(message=f"[paignion] {message}", color="red"), end=end)
    exit(1)
