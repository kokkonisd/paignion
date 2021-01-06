import os


__version__ = "0.0.1"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, os.pardir, "frontend")


DIRECTIONS = [
    "north",
    "east",
    "south",
    "west",
    "up",
    "down",
]

MD_EXTENSIONS = [
    "pymdownx.tilde",
    "pymdownx.emoji",
]


SIMPLE_ORIGIN_ROOM_TEMPLATE = """\
---
## Paignion v{}
##
## This is a template for a basic origin room in Paignion.
## There must always be exactly one origin room in a Paignion game; this is the room
## where the player starts in when they launch the game.
##
## Room files, as you can see, are split into two parts: a YAML header and a Markdown
## body. The YAML head is enclosed in three dashes (-) and must always be present, even
## if it is empty. In the YAML part you can define a room's metadata; the rooms it
## links to, the items it contains, the properties of these items etc. The Markdown
## body contains the description of the room, which the player sees whenever they enter
## it.
##
## As you can see below, you do not need to define all directions, you just need to
## define the ones you are going to use. In this example, at the east of this room we
## find the second room of the game, which means that if the player writes `go east`
## from this room then they will move to that second room. The possible directions are
## north, east, south, west, up and down. You can not define some or all directions and
## fill them in dynamically via actions later (see the `complete_demo` example game and
## the README for more info).
east: second_room
items:
    intangible:
        - name: painting
          description: A gorgeous painting.
    tangible:
        - name: book
          description: An old, dusty book.
---

This is the start room. There is a painting on the wall and a book on the _floor_.
"""


SIMPLE_SECOND_ROOM_TEMPLATE = """\
---
## Paignion v{}
##
## This is a template for a basic second room in Paignion.
west: origin
---

This is the second room. Not much going on here.
"""
