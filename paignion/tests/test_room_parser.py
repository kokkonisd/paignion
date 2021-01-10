import unittest
import json
import os

from paignion.parser import PaignionParser
from paignion.exceptions import PaignionException

TEST_DATA_DIR = "paignion/tests/test_data"
ROOMS_OK_DIR = os.path.join(TEST_DATA_DIR, "rooms_ok")
ROOMS_KO_DIR = os.path.join(TEST_DATA_DIR, "rooms_ko")


class TestRoomParser(unittest.TestCase):
    def test_minimal_room(self):
        self.maxDiff = None
        parser = PaignionParser()

        with open(os.path.join(ROOMS_OK_DIR, "minimal_room.md"), "r") as f:
            room = parser.parse_room_data(room_data=f.read(), room_name="minimal_room")

        with open(os.path.join(ROOMS_OK_DIR, "expected_minimal_room.json")) as f:
            expected_room = f.read()[:-1]  # Omit the newline at the end

        self.assertEqual(json.dumps(room, indent=4, sort_keys=True), expected_room)

    def test_simple_direction(self):
        self.maxDiff = None
        parser = PaignionParser()

        with open(os.path.join(ROOMS_OK_DIR, "simple_direction_room.md"), "r") as f:
            room = parser.parse_room_data(
                room_data=f.read(), room_name="simple_direction_room"
            )

        with open(
            os.path.join(ROOMS_OK_DIR, "expected_simple_direction_room.json")
        ) as f:
            expected_room = f.read()[:-1]  # Omit the newline at the end

        self.assertEqual(json.dumps(room, indent=4, sort_keys=True), expected_room)

    def test_full_directions(self):
        self.maxDiff = None
        parser = PaignionParser()

        with open(os.path.join(ROOMS_OK_DIR, "full_directions_room.md"), "r") as f:
            room = parser.parse_room_data(
                room_data=f.read(), room_name="full_directions_room"
            )

        with open(
            os.path.join(ROOMS_OK_DIR, "expected_full_directions_room.json")
        ) as f:
            expected_room = f.read()[:-1]  # Omit the newline at the end

        self.assertEqual(json.dumps(room, indent=4, sort_keys=True), expected_room)

    def test_tangible_items(self):
        self.maxDiff = None
        parser = PaignionParser()

        with open(os.path.join(ROOMS_OK_DIR, "tangible_items_room.md"), "r") as f:
            room = parser.parse_room_data(
                room_data=f.read(), room_name="tangible_items_room"
            )

        with open(os.path.join(ROOMS_OK_DIR, "expected_tangible_items_room.json")) as f:
            expected_room = f.read()[:-1]  # Omit the newline at the end

        self.assertEqual(json.dumps(room, indent=4, sort_keys=True), expected_room)

    def test_intangible_items(self):
        self.maxDiff = None
        parser = PaignionParser()

        with open(os.path.join(ROOMS_OK_DIR, "intangible_items_room.md"), "r") as f:
            room = parser.parse_room_data(
                room_data=f.read(), room_name="intangible_items_room"
            )

        with open(
            os.path.join(ROOMS_OK_DIR, "expected_intangible_items_room.json")
        ) as f:
            expected_room = f.read()[:-1]  # Omit the newline at the end

        self.assertEqual(json.dumps(room, indent=4, sort_keys=True), expected_room)

    def test_full_items(self):
        self.maxDiff = None
        parser = PaignionParser()

        with open(os.path.join(ROOMS_OK_DIR, "full_items_room.md"), "r") as f:
            room = parser.parse_room_data(
                room_data=f.read(), room_name="full_items_room"
            )

        with open(os.path.join(ROOMS_OK_DIR, "expected_full_items_room.json")) as f:
            expected_room = f.read()[:-1]  # Omit the newline at the end

        self.assertEqual(json.dumps(room, indent=4, sort_keys=True), expected_room)
