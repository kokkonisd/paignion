import pytest

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


class TestRoomObject:
    def test_room_defaults(self):
        room = PaignionRoom(name="test name", description="test description")

        assert room.name == "test name"
        assert room.description == "test description"
        assert room.north == None
        assert room.east == None
        assert room.south == None
        assert room.west == None
        assert room.up == None
        assert room.down == None
        assert room.tangible_items == []
        assert room.intangible_items == []

    def test_missing_name_and_description(self):
        with pytest.raises(
            TypeError,
            match=r".+ missing 2 required positional arguments: 'name' and "
            r"'description'",
        ):
            room = PaignionRoom()

        with pytest.raises(
            TypeError, match=r".+ missing 1 required positional argument: 'description'"
        ):
            room = PaignionRoom(name="test name")

        with pytest.raises(
            TypeError, match=r".+ missing 1 required positional argument: 'name'"
        ):
            room = PaignionRoom(description="test description")

        with pytest.raises(PaignionRoomException, match=r"Name missing for room"):
            room = PaignionRoom(name=None, description="test description")

        with pytest.raises(
            PaignionRoomException, match=r"Description missing for room `test name`"
        ):
            room = PaignionRoom(name="test name", description=None)

        with pytest.raises(PaignionRoomException, match=r"Name missing for room"):
            room = PaignionRoom(name=None, description=None)

    def test_passing_nonlists_to_tangible_and_intangible_items(self):
        with pytest.raises(
            PaignionRoomException,
            match=r"Tangible items should be a list for room `test name`",
        ):
            room = PaignionRoom(
                name="test name", description="test description", tangible_items=1
            )

        with pytest.raises(
            PaignionRoomException,
            match=r"Intangible items should be a list for room `test name`",
        ):
            room = PaignionRoom(
                name="test name",
                description="test description",
                intangible_items=PaignionItem(
                    name="test item name", description="test item description"
                ),
            )

    def test_passing_lists_of_wrong_type_to_tangible_and_intangible_items(self):
        with pytest.raises(
            PaignionRoomException,
            match=r"Item `1` has incorrect type for room `test name`",
        ):
            room = PaignionRoom(
                name="test name",
                description="test description",
                tangible_items=[1, 2, 3],
            )

        with pytest.raises(
            PaignionRoomException,
            match=r"Item `abc` has incorrect type for room `test name`",
        ):
            room = PaignionRoom(
                name="test name",
                description="test description",
                tangible_items=["abc", "def", "ghi"],
            )

    def test_dump(self):
        self.maxDiff = None

        room = PaignionRoom(name="test name", description="test description")

        assert str(room) == EXPECTED_DEFAULT_ROOM_DUMP
