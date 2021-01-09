import json

from paignion.exceptions import PaignionRoomException
from paignion.item import PaignionItem


class PaignionRoom(object):
    """Describe a Paignion room."""

    def __init__(
        self,
        name,
        description,
        north=None,
        east=None,
        south=None,
        west=None,
        up=None,
        down=None,
        tangible_items=None,
        intangible_items=None,
    ):
        """Construct a new instance of PaignionRoom.

        :param name: the name of the room
        :type name: str
        :param description: the description of the room
        :type description: str
        :param north: the room to the north of this room
        :type north: str
        :param east: the room to the east of this room
        :type east: str
        :param south: the room to the south of this room
        :type south: str
        :param west: the room to the west of this room
        :type west: str
        :param up: the room to the up direction of this room
        :type up: str
        :param down: the room to the down direction of this room
        :type down: str
        :param tangible_items: a list of tangible items found in the room
        :type tangible_items: list
        :param intangible_items: a list of intangible items found in the room
        :type intangible_items: list
        :return: an instance of PaignionRoom
        """
        self.name = name
        self.description = description
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.up = up
        self.down = down
        self.tangible_items = tangible_items
        self.intangible_items = intangible_items

        self.verify_attributes()

    def verify_attributes(self):
        """Verify the attributes of the PaignionRoom object."""
        # Tangible items should be an empty list by default
        self.tangible_items = [] if not self.tangible_items else self.tangible_items
        # Intangible items should be an empty list by default
        self.intangible_items = (
            [] if not self.intangible_items else self.intangible_items
        )

        # Room name is mandatory
        if not self.name:
            raise PaignionRoomException("Name missing for room")

        # Room description is mandatory
        if not self.description:
            raise PaignionRoomException(f"Description missing for room `{self.name}`")

        # Tangible items should be list
        if type(self.tangible_items) != list:
            raise PaignionRoomException(
                f"Tangible items should be a list for room `{self.name}`"
            )

        # Intangible items should be list
        if type(self.intangible_items) != list:
            raise PaignionRoomException(
                f"Intangible items should be a list for room `{self.name}`"
            )

        # Tangible & intangible items should be lists of PaignionItems
        for i in self.tangible_items + self.tangible_items:
            if type(i) != PaignionItem:
                raise PaignionRoomException(
                    f"Item `{i}` has incorrect type for room `{self.name}`"
                )

    def dump(self):
        """Dump a dictionary containing all of the data of the room.

        :return: a dictionary containing the room's data
        """
        return {
            self.name: {
                "north": self.north,
                "east": self.east,
                "south": self.south,
                "west": self.west,
                "up": self.up,
                "down": self.down,
                "description": self.description,
                "items": {
                    "tangible": [i.dump() for i in self.tangible_items],
                    "intangible": [i.dump() for i in self.intangible_items],
                },
            }
        }

    def __str__(self):
        return json.dumps(self.dump(), indent=4, sort_keys=True)
