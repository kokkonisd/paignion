import markdown


from paignion.definitions import MD_EXTENSIONS


def markdownify(string):
    if not string:
        return string

    return markdown.markdown(string, extensions=MD_EXTENSIONS)
