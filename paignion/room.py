import json


from paignion.exception import PaignionException


class PaignionRoom(object):
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
        # Tangible items should be an empty list by default
        self.tangible_items = [] if not self.tangible_items else self.tangible_items
        # Intangible items should be an empty list by default
        self.intangible_items = (
            [] if not self.intangible_items else self.intangible_items
        )

        # Item name is mandatory
        if not self.name:
            raise PaignionException("Name missing for item")

        # Item description is mandatory
        if not self.description:
            raise PaignionException(f"Description missing for item `{self.name}`")

    def dump(self):
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
        return json.dumps(self.dump(), indent=4)
