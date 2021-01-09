import unittest

from paignion.room import PaignionRoom
from paignion.exceptions import PaignionRoomException


EXPECTED_DEFAULT_ROOM_DUMP = """\
{
    "test name": {
        "description": "test description",
        "down": null,
        "east": null,
        "items": {
            "intangible": [],
            "tangible": []
        },
        "north": null,
        "south": null,
        "up": null,
        "west": null
    }
}\
"""


class TestRoomObject(unittest.TestCase):
    def test_room_defaults(self):
        room = PaignionRoom(name="test name", description="test description")

        self.assertEqual(room.name, "test name")
        self.assertEqual(room.description, "test description")
        self.assertEqual(room.north, None)
        self.assertEqual(room.east, None)
        self.assertEqual(room.south, None)
        self.assertEqual(room.west, None)
        self.assertEqual(room.up, None)
        self.assertEqual(room.down, None)
        self.assertEqual(room.tangible_items, [])
        self.assertEqual(room.intangible_items, [])

    def test_missing_name_and_description(self):
        with self.assertRaises(TypeError):
            room = PaignionRoom()

        with self.assertRaises(TypeError):
            room = PaignionRoom(name="test name")

        with self.assertRaises(TypeError):
            room = PaignionRoom(description="test description")

        with self.assertRaises(PaignionRoomException):
            room = PaignionRoom(name=None, description="test description")

        with self.assertRaises(PaignionRoomException):
            room = PaignionRoom(name="test name", description=None)

        with self.assertRaises(PaignionRoomException):
            room = PaignionRoom(name=None, description=None)

    def test_dump(self):
        self.maxDiff = None

        room = PaignionRoom(name="test name", description="test description")

        self.assertEqual(str(room), EXPECTED_DEFAULT_ROOM_DUMP)
