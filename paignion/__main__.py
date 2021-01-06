#!/usr/bin/env python3

import argparse
import subprocess
import os
import glob
import json


from paignion.definitions import (
    FRONTEND_DIR,
    SIMPLE_ORIGIN_ROOM_TEMPLATE,
    SIMPLE_SECOND_ROOM_TEMPLATE,
    __version__,
)
from paignion.parser import PaignionParser


def paignion_init(namespace):
    project_dir = namespace.project_dir

    print(f"Initializing new Paignion game at directory {project_dir}")
    subprocess.run(["mkdir", "-p", project_dir], stdout=subprocess.PIPE)
    subprocess.run(
        ["mkdir", "-p", os.path.join(project_dir, "rooms")], stdout=subprocess.PIPE
    )

    with open(os.path.join(project_dir, "rooms", "origin.md"), "w") as map_file:
        map_file.write(SIMPLE_ORIGIN_ROOM_TEMPLATE.format(__version__))

    with open(os.path.join(project_dir, "rooms", "second_room.md"), "w") as map_file:
        map_file.write(SIMPLE_SECOND_ROOM_TEMPLATE.format(__version__))


def paignion_build(namespace):
    parser = PaignionParser()

    parser.verify_project_dir(namespace.project_dir)

    room_files = [
        f for f in glob.glob(os.path.join(namespace.project_dir, "rooms", "*.md"))
    ]

    # Generate final GAME_DATA object
    GAME_DATA = parser.parse_room_files(room_files)

    build_dir = os.path.join(namespace.project_dir, "build")
    print(f"Building project {namespace.project_dir}")
    subprocess.run(["mkdir", "-p", build_dir], stdout=subprocess.PIPE)
    subprocess.run(
        [
            "cp",
            os.path.join(FRONTEND_DIR, "index.html"),
            os.path.join(FRONTEND_DIR, "main.css"),
            os.path.join(FRONTEND_DIR, "paignion.js"),
            build_dir,
        ],
        stdout=subprocess.PIPE,
    )

    # Put game data into the generated paignion.js file
    with open(os.path.join(build_dir, "paignion.js"), "a") as f:
        f.write("\n\n\n// Automatically generated game data object\n")
        f.write(f"let GAME_DATA = {json.dumps(GAME_DATA)};")

    print("Done")


def paignion_main_function():
    parser = argparse.ArgumentParser(description="A text adventure game engine")
    subparsers = parser.add_subparsers(
        help="Run `paignion init <game_dir>` to start a new game project, or "
        "`paignion build <game_dir>` to build game files into a playable game"
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
        help="Show the version of Paignion and exit",
    )

    parser_init = subparsers.add_parser("init", help="Create a new game project")
    parser_init.set_defaults(func=paignion_init)
    parser_init.add_argument(
        "project_dir", help="The project directory (to be created if it doesn't exist)"
    )

    parser_build = subparsers.add_parser(
        "build", help="Build an existing game project into a playable game"
    )
    parser_build.set_defaults(func=paignion_build)
    parser_build.add_argument(
        "project_dir", help="The directory containing the project files"
    )

    args = parser.parse_args()
    if "func" not in args:
        # No valid sub-command was provided, show help
        parser.print_help()
        exit(0)

    args.func(args)


if __name__ == "__main__":
    paignion_main_function()
