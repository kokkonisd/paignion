import re
import os
import json
import yaml

from paignion.definitions import DIRECTIONS
from paignion.exceptions import (
    PaignionException,
    PaignionRoomException,
    PaignionItemException,
    PaignionUsedWithItemException,
)
from paignion.room import PaignionRoom
from paignion.item import PaignionItem
from paignion.used_with_item import PaignionUsedWithItem
from paignion.tools import markdownify


class PaignionParser(object):
    """Parse Paignion room files.

    This class is responsible for parsing Paignion room files and generating a
    GAME_DATA object containing all of the game data that was derived from the files.
    This object is then ready to be injected into the frontend engine to produce a
    working game.
    """

    def verify_project_dir(self, project_dir):
        """Verify the structure & contents of a project directory.

        :param project_dir: the directory of the project directory
        :type project_dir: str
        """
        rooms_dir = os.path.join(project_dir, "rooms")
        origin_room = os.path.join(rooms_dir, "origin.md")

        # Check that the rooms directory exists
        if not os.path.exists(rooms_dir) or not os.path.isdir(rooms_dir):
            raise PaignionException(
                "Rooms directory not found. Please create the rooms/ directory."
            )

        # Check that the origin.md room exists
        if not os.path.exists(origin_room) or not os.path.isfile(origin_room):
            raise PaignionException(
                "Origin room (origin.md) not found. Please create an origin room."
            )

    def parse_room_files(self, room_files):
        """Parse a list of Paignion room files and generate the GAME_DATA object.

        Parse a series of room files and merge the results to derive the final
        GAME_DATA object containing all of the relevant game info needed by the
        frontend engine.

        :param room_files: a list of the paths to the room files
        :type room_files: list
        """
        room_data = {}

        for room_file in room_files:
            with open(room_file, "r") as f:
                room_data.update(
                    self.parse_room_data(
                        room_data=f.read(),
                        room_name=os.path.splitext(room_file)[0].split("/")[-1],
                    )
                )

        return room_data

    def parse_room_data(self, room_data, room_name):
        """Parse a single room file.

        Parses the YAML header and the Markdown body of a room file and generates a
        Room object, containing all of the relevant info about the room.

        :param room_data: the raw data of the room file
        :type room_data: str
        :param room_name: the name of the room
        :type room_name: str
        :return: a dict containing the data of the room
        """
        # Detect YAML part
        frontmatter_match = re.search("---\n(((?!---)[\\s\\S])*)---", room_data)

        # Parse YAML part
        frontmatter = yaml.load(frontmatter_match.group(1), Loader=yaml.Loader)
        # If the YAML is empty, replace it by an empty dict
        if not frontmatter:
            frontmatter = {}

        # Parse Markdown part
        md = markdownify(room_data[frontmatter_match.span()[1] :])

        # Parse items
        if "items" in frontmatter:
            # Parse tangible items
            tangible_items = []
            # If there are no tangible items, the next loop should not run
            raw_tangible_items = (
                frontmatter["items"]["tangible"]
                if "tangible" in frontmatter["items"]
                else []
            )
            # Iterate over tangible items
            for tangible_item in raw_tangible_items:
                # Parse used_with items
                if "used_with" in tangible_item:
                    used_with = []
                    for uw_item in tangible_item["used_with"]:
                        try:
                            used_with.append(
                                PaignionUsedWithItem(
                                    name=uw_item.get("name"),
                                    effect_message=markdownify(
                                        uw_item.get("effect_message")
                                    ),
                                    consumes_subject=uw_item.get("consumes_subject"),
                                    consumes_object=uw_item.get("consumes_object"),
                                    actions=uw_item.get("actions"),
                                )
                            )
                        except PaignionUsedWithItemException:
                            raise PaignionException(
                                f"Could not parse used_with item for tangible item "
                                f"`{tangible_item.get('name')}` in room `{room_name}`"
                            )
                else:
                    used_with = []

                try:
                    tangible_items.append(
                        PaignionItem(
                            name=tangible_item.get("name"),
                            description=markdownify(tangible_item.get("description")),
                            amount=tangible_item.get("amount"),
                            visible=tangible_item.get("visible"),
                            effect=tangible_item.get("effect"),
                            used_with=used_with,
                        )
                    )
                except PaignionItemException:
                    raise PaignionException(
                        f"Could not parse tangible item in room `{room_name}`"
                    )

            # Parse intangible items
            intangible_items = []
            # If there are no intangible items, the next loop should not run
            raw_intangible_items = (
                frontmatter["items"]["intangible"]
                if "intangible" in frontmatter["items"]
                else []
            )
            # Iterate over intangible items
            for intangible_item in raw_intangible_items:
                # Parse used_with items
                if "used_with" in intangible_item:
                    used_with = []
                    for uw_item in intangible_item["used_with"]:
                        try:
                            used_with.append(
                                PaignionUsedWithItem(
                                    name=uw_item.get("name"),
                                    effect_message=markdownify(
                                        uw_item.get("effect_message")
                                    ),
                                    consumes_subject=uw_item.get("consumes_subject"),
                                    consumes_object=uw_item.get("consumes_object"),
                                    actions=uw_item.get("actions"),
                                )
                            )
                        except PaignionUsedWithItemException:
                            raise PaignionException(
                                f"Could not parse used_with item for intangible item "
                                f"`{intangible_item['name']}` in room `{room_name}`"
                            )
                else:
                    used_with = []

                try:
                    intangible_items.append(
                        PaignionItem(
                            name=intangible_item.get("name"),
                            description=markdownify(intangible_item.get("description")),
                            amount=intangible_item.get("amount"),
                            visible=intangible_item.get("visible"),
                            effect=intangible_item.get("effect"),
                            used_with=used_with,
                        )
                    )
                except PaignionItemException:
                    raise PaignionException(
                        f"Could not parse intangible item in room `{room_name}`"
                    )
        else:
            tangible_items = []
            intangible_items = []

        # Create room
        try:
            room = PaignionRoom(
                name=room_name,
                description=md,
                north=frontmatter.get("north"),
                east=frontmatter.get("east"),
                south=frontmatter.get("south"),
                west=frontmatter.get("west"),
                up=frontmatter.get("up"),
                down=frontmatter.get("down"),
                tangible_items=tangible_items,
                intangible_items=intangible_items,
            )
        except PaignionRoomException:
            raise PaignionException(f"Could not parse room `{room_name}`")

        return room.dump()
