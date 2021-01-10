import pytest
import json
import os

from paignion.parser import PaignionParser
from paignion.exceptions import PaignionException

TEST_DATA_DIR = "tests/test_data"
ROOMS_OK_DIR = os.path.join(TEST_DATA_DIR, "rooms_ok")
ROOMS_KO_DIR = os.path.join(TEST_DATA_DIR, "rooms_ko")


class TestRoomParser:
    def test_minimal_room(self):
        parser = PaignionParser()

        with open(os.path.join(ROOMS_OK_DIR, "minimal_room.md"), "r") as f:
            room = parser.parse_room_data(room_data=f.read(), room_name="minimal_room")

        with open(os.path.join(ROOMS_OK_DIR, "expected_minimal_room.json")) as f:
            expected_room = f.read()[:-1]  # Omit the newline at the end

        assert json.dumps(room, indent=4, sort_keys=True) == expected_room

    def test_simple_direction(self):
        parser = PaignionParser()

        with open(os.path.join(ROOMS_OK_DIR, "simple_direction_room.md"), "r") as f:
            room = parser.parse_room_data(
                room_data=f.read(), room_name="simple_direction_room"
            )

        with open(
            os.path.join(ROOMS_OK_DIR, "expected_simple_direction_room.json")
        ) as f:
            expected_room = f.read()[:-1]  # Omit the newline at the end

        assert json.dumps(room, indent=4, sort_keys=True) == expected_room

    def test_full_directions(self):
        parser = PaignionParser()

        with open(os.path.join(ROOMS_OK_DIR, "full_directions_room.md"), "r") as f:
            room = parser.parse_room_data(
                room_data=f.read(), room_name="full_directions_room"
            )

        with open(
            os.path.join(ROOMS_OK_DIR, "expected_full_directions_room.json")
        ) as f:
            expected_room = f.read()[:-1]  # Omit the newline at the end

        assert json.dumps(room, indent=4, sort_keys=True) == expected_room

    def test_tangible_items(self):
        parser = PaignionParser()

        with open(os.path.join(ROOMS_OK_DIR, "tangible_items_room.md"), "r") as f:
            room = parser.parse_room_data(
                room_data=f.read(), room_name="tangible_items_room"
            )

        with open(os.path.join(ROOMS_OK_DIR, "expected_tangible_items_room.json")) as f:
            expected_room = f.read()[:-1]  # Omit the newline at the end

        assert json.dumps(room, indent=4, sort_keys=True) == expected_room

    def test_intangible_items(self):
        parser = PaignionParser()

        with open(os.path.join(ROOMS_OK_DIR, "intangible_items_room.md"), "r") as f:
            room = parser.parse_room_data(
                room_data=f.read(), room_name="intangible_items_room"
            )

        with open(
            os.path.join(ROOMS_OK_DIR, "expected_intangible_items_room.json")
        ) as f:
            expected_room = f.read()[:-1]  # Omit the newline at the end

        assert json.dumps(room, indent=4, sort_keys=True) == expected_room

    def test_full_items(self):
        parser = PaignionParser()

        with open(os.path.join(ROOMS_OK_DIR, "full_items_room.md"), "r") as f:
            room = parser.parse_room_data(
                room_data=f.read(), room_name="full_items_room"
            )

        with open(os.path.join(ROOMS_OK_DIR, "expected_full_items_room.json")) as f:
            expected_room = f.read()[:-1]  # Omit the newline at the end

        assert json.dumps(room, indent=4, sort_keys=True) == expected_room

    def test_missing_description(self):
        parser = PaignionParser()

        with open(os.path.join(ROOMS_KO_DIR, "missing_description.md"), "r") as f:
            room_data = f.read()

        with pytest.raises(
            PaignionException,
            match=r"Could not parse room `missing_description`",
        ):
            parser.parse_room_data(room_data=room_data, room_name="missing_description")

    def test_missing_tangible_item_name(self):
        parser = PaignionParser()

        with open(
            os.path.join(ROOMS_KO_DIR, "missing_tangible_item_name.md"), "r"
        ) as f:
            room_data = f.read()

        with pytest.raises(
            PaignionException,
            match=r"Could not parse tangible item in room "
            r"`missing_tangible_item_name`",
        ):
            parser.parse_room_data(
                room_data=room_data, room_name="missing_tangible_item_name"
            )

    def test_missing_tangible_item_description(self):
        parser = PaignionParser()

        with open(
            os.path.join(ROOMS_KO_DIR, "missing_tangible_item_description.md"), "r"
        ) as f:
            room_data = f.read()

        with pytest.raises(
            PaignionException,
            match=r"Could not parse tangible item in room "
            r"`missing_tangible_item_description`",
        ):
            parser.parse_room_data(
                room_data=room_data, room_name="missing_tangible_item_description"
            )

    def test_missing_intangible_item_name(self):
        parser = PaignionParser()

        with open(
            os.path.join(ROOMS_KO_DIR, "missing_intangible_item_name.md"), "r"
        ) as f:
            room_data = f.read()

        with pytest.raises(
            PaignionException,
            match=r"Could not parse intangible item in room "
            r"`missing_intangible_item_name`",
        ):
            parser.parse_room_data(
                room_data=room_data, room_name="missing_intangible_item_name"
            )

    def test_missing_intangible_item_description(self):
        parser = PaignionParser()

        with open(
            os.path.join(ROOMS_KO_DIR, "missing_intangible_item_description.md"), "r"
        ) as f:
            room_data = f.read()

        with pytest.raises(
            PaignionException,
            match=r"Could not parse intangible item in room "
            r"`missing_intangible_item_description`",
        ):
            parser.parse_room_data(
                room_data=room_data, room_name="missing_intangible_item_description"
            )

    def test_missing_tangible_used_with_item_name(self):
        parser = PaignionParser()

        with open(
            os.path.join(ROOMS_KO_DIR, "missing_tangible_used_with_item_name.md"), "r"
        ) as f:
            room_data = f.read()

        with pytest.raises(
            PaignionException,
            match=r"Could not parse used_with item for tangible item `test` in room "
            r"`missing_tangible_used_with_item_name`",
        ):
            parser.parse_room_data(
                room_data=room_data, room_name="missing_tangible_used_with_item_name"
            )

    def test_missing_tangible_used_with_item_effect_message(self):
        parser = PaignionParser()

        with open(
            os.path.join(
                ROOMS_KO_DIR, "missing_tangible_used_with_item_effect_message.md"
            ),
            "r",
        ) as f:
            room_data = f.read()

        with pytest.raises(
            PaignionException,
            match=r"Could not parse used_with item for tangible item `test` in room "
            r"`missing_tangible_used_with_item_effect_message`",
        ):
            parser.parse_room_data(
                room_data=room_data,
                room_name="missing_tangible_used_with_item_effect_message",
            )

    def test_missing_intangible_used_with_item_name(self):
        parser = PaignionParser()

        with open(
            os.path.join(ROOMS_KO_DIR, "missing_intangible_used_with_item_name.md"), "r"
        ) as f:
            room_data = f.read()

        with pytest.raises(
            PaignionException,
            match=r"Could not parse used_with item for intangible item `test` in room "
            r"`missing_intangible_used_with_item_name`",
        ):
            parser.parse_room_data(
                room_data=room_data, room_name="missing_intangible_used_with_item_name"
            )

    def test_missing_intangible_used_with_item_effect_message(self):
        parser = PaignionParser()

        with open(
            os.path.join(
                ROOMS_KO_DIR, "missing_intangible_used_with_item_effect_message.md"
            ),
            "r",
        ) as f:
            room_data = f.read()

        with pytest.raises(
            PaignionException,
            match=r"Could not parse used_with item for intangible item `test` in room "
            r"`missing_intangible_used_with_item_effect_message`",
        ):
            parser.parse_room_data(
                room_data=room_data,
                room_name="missing_intangible_used_with_item_effect_message",
            )
