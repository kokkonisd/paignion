from paignion.tools import color_message


class PaignionException(Exception):
    def __init__(self, message):
        super().__init__(color_message(message, color="red"))


class PaignionRoomException(PaignionException):
    pass


class PaignionItemException(PaignionException):
    pass


class PaignionUsedWithItemException(PaignionException):
    pass


class PaignionActionCompilerException(PaignionException):
    pass
