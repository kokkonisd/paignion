import re
import os
import json
import yaml
import markdown

from paignion.definitions import DIRECTIONS, MD_EXTENSIONS
from paignion.exception import PaignionException
from paignion.room import PaignionRoom
from paignion.item import PaignionItem
from paignion.used_with_item import PaignionUsedWithItem


class PaignionParser(object):
    def verify_project_dir(self, project_dir):
        rooms_dir = os.path.join(project_dir, "rooms")

        # Check that the rooms directory exists
        if not os.path.exists(rooms_dir) or not os.path.isdir(rooms_dir):
            raise PaignionException(
                "Rooms directory not found. Please create the rooms/ directory."
            )

    def parse_room_files(self, room_files):
        room_data = {}

        for room_file in room_files:
            with open(room_file, "r") as f:
                room_data.update(
                    self.parse_room_file(
                        room_data=f.read(),
                        room_name=os.path.splitext(room_file)[0].split("/")[-1],
                    )
                )

        return room_data

    def markdownify(self, string):
        if not string:
            return string

        return markdown.markdown(string, extensions=MD_EXTENSIONS)

    def parse_room_file(self, room_data, room_name):
        # Detect YAML part
        frontmatter_match = re.search("---\n(((?!---)[\\s\\S])*)---", room_data)

        # Parse YAML part
        frontmatter = yaml.load(frontmatter_match.group(1), Loader=yaml.Loader)
        # If the YAML is empty, replace it by an empty dict
        if not frontmatter:
            frontmatter = {}

        # Parse Markdown part
        md = self.markdownify(room_data[frontmatter_match.span()[1] :])

        # Parse items
        if "items" in frontmatter:
            # Parse tangible items
            tangible_items = []
            raw_tangible_items = (
                frontmatter["items"]["tangible"]
                if "tangible" in frontmatter["items"]
                else []
            )
            for tangible_item in raw_tangible_items:
                # Parse used_with items
                if "used_with" in tangible_item:
                    used_with = []
                    for uw_item in tangible_item["used_with"]:
                        try:
                            used_with.append(
                                PaignionUsedWithItem(
                                    name=uw_item.get("name"),
                                    effect_message=self.markdownify(
                                        uw_item.get("effect_message")
                                    ),
                                    consumes_subject=uw_item.get("consumes_subject"),
                                    consumes_object=uw_item.get("consumes_object"),
                                    actions=uw_item.get("actions"),
                                )
                            )
                        except PaignionException:
                            raise PaignionException(
                                f"Error parsing used_with item for tangible item"
                                f"`{tangible_item.get('name')}` in room `{room_name}`"
                            )
                else:
                    used_with = []

                try:
                    tangible_items.append(
                        PaignionItem(
                            name=tangible_item.get("name"),
                            description=self.markdownify(
                                tangible_item.get("description")
                            ),
                            amount=tangible_item.get("amount"),
                            visible=tangible_item.get("visible"),
                            effect=tangible_item.get("effect"),
                            used_with=used_with,
                        )
                    )
                except PaignionException:
                    raise PaignionException(
                        f"Error parsing tangible item `{tangible_item.get('name')}` in"
                        f"room `{room_name}`"
                    )

            # Parse intangible items
            intangible_items = []
            raw_intangible_items = (
                frontmatter["items"]["intangible"]
                if "intangible" in frontmatter["items"]
                else []
            )
            for intangible_item in raw_intangible_items:
                # Parse used_with items
                if "used_with" in intangible_item:
                    used_with = []
                    for uw_item in intangible_item["used_with"]:
                        try:
                            used_with.append(
                                PaignionUsedWithItem(
                                    name=uw_item.get("name"),
                                    effect_message=self.markdownify(
                                        uw_item.get("effect_message")
                                    ),
                                    consumes_subject=uw_item.get("consumes_subject"),
                                    consumes_object=uw_item.get("consumes_object"),
                                    actions=uw_item.get("actions"),
                                )
                            )
                        except PaignionException:
                            raise PaignionException(
                                f"Error parsing used_with item for intangible item"
                                f"`{intangible_item}` in room `{room_name}`"
                            )
                else:
                    used_with = []

                try:
                    intangible_items.append(
                        PaignionItem(
                            name=intangible_item.get("name"),
                            description=self.markdownify(
                                intangible_item.get("description")
                            ),
                            amount=intangible_item.get("amount"),
                            visible=intangible_item.get("visible"),
                            effect=intangible_item.get("effect"),
                            used_with=used_with,
                        )
                    )
                except PaignionException:
                    raise PaignionException(
                        f"Error parsing intangible item `{intangible_item.get('name')}`"
                        f" in room `{room_name}`"
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
        except PaignionException:
            raise PaignionException(f"Error parsing room `{room_name}`")

        return room.dump()
