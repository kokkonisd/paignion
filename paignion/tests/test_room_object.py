import unittest

from paignion.room import PaignionRoom
from paignion.item import PaignionItem
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
        with self.assertRaises(TypeError) as err:
            room = PaignionRoom()

        self.assertEqual(
            str(err.exception),
            "__init__() missing 2 required positional arguments: 'name' and "
            "'description'",
        )

        with self.assertRaises(TypeError) as err:
            room = PaignionRoom(name="test name")

        self.assertEqual(
            str(err.exception),
            "__init__() missing 1 required positional argument: 'description'",
        )

        with self.assertRaises(TypeError) as err:
            room = PaignionRoom(description="test description")

        self.assertEqual(
            str(err.exception),
            "__init__() missing 1 required positional argument: 'name'",
        )

        with self.assertRaises(PaignionRoomException) as err:
            room = PaignionRoom(name=None, description="test description")

        self.assertEqual(
            str(err.exception),
            "Name missing for room",
        )

        with self.assertRaises(PaignionRoomException) as err:
            room = PaignionRoom(name="test name", description=None)

        self.assertEqual(
            str(err.exception),
            "Description missing for room `test name`",
        )

        with self.assertRaises(PaignionRoomException) as err:
            room = PaignionRoom(name=None, description=None)

        self.assertEqual(
            str(err.exception),
            "Name missing for room",
        )

    def test_passing_nonlists_to_tangible_and_intangible_items(self):
        with self.assertRaises(PaignionRoomException) as err:
            room = PaignionRoom(
                name="test name", description="test description", tangible_items=1
            )

        self.assertEqual(
            str(err.exception), "Tangible items should be a list for room `test name`"
        )

        with self.assertRaises(PaignionRoomException) as err:
            room = PaignionRoom(
                name="test name",
                description="test description",
                intangible_items=PaignionItem(
                    name="test item name", description="test item description"
                ),
            )

        self.assertEqual(
            str(err.exception), "Intangible items should be a list for room `test name`"
        )

    def test_passing_lists_of_wrong_type_to_tangible_and_intangible_items(self):
        with self.assertRaises(PaignionRoomException) as err:
            room = PaignionRoom(
                name="test name",
                description="test description",
                tangible_items=[1, 2, 3],
            )

        self.assertEqual(
            str(err.exception), "Item `1` has incorrect type for room `test name`"
        )

        with self.assertRaises(PaignionRoomException) as err:
            room = PaignionRoom(
                name="test name",
                description="test description",
                tangible_items=["abc", "def", "ghi"],
            )

        self.assertEqual(
            str(err.exception), "Item `abc` has incorrect type for room `test name`"
        )

    def test_dump(self):
        self.maxDiff = None

        room = PaignionRoom(name="test name", description="test description")

        self.assertEqual(str(room), EXPECTED_DEFAULT_ROOM_DUMP)
