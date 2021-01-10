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
    INDEX_HTML_TEMPLATE,
    __version__,
)
from paignion.parser import PaignionParser
from paignion.tools import info
from paignion.exceptions import PaignionException


def paignion_init(namespace):
    """Initialize a Paignion game project with the appropriate files & directories."""
    project_dir = namespace.project_dir

    # Create the project directory if it does not exist
    subprocess.run(["mkdir", "-p", project_dir], stdout=subprocess.PIPE)
    # Create the rooms directory in the project dir, to contain the room files
    subprocess.run(
        ["mkdir", "-p", os.path.join(project_dir, "rooms")], stdout=subprocess.PIPE
    )

    # Dump the origin room using the origin room template
    with open(os.path.join(project_dir, "rooms", "origin.md"), "w") as map_file:
        map_file.write(SIMPLE_ORIGIN_ROOM_TEMPLATE.format(__version__))

    # Dump the second room using the second room template
    with open(os.path.join(project_dir, "rooms", "second_room.md"), "w") as map_file:
        map_file.write(SIMPLE_SECOND_ROOM_TEMPLATE.format(__version__))

    info(f"Initialized new Paignion game at `{project_dir}`")


def paignion_build(namespace):
    """Build a Paignion game project into a playable game."""
    parser = PaignionParser()

    # Check the structure of the project dir for errors
    try:
        parser.verify_project_dir(namespace.project_dir)
    except PaignionException:
        raise PaignionException(f"Invalid project directory `{namespace.project_dir}`")

    # Collect room files
    room_files = [
        f for f in glob.glob(os.path.join(namespace.project_dir, "rooms", "*.md"))
    ]

    # Generate final GAME_DATA object
    GAME_DATA = parser.parse_room_files(room_files)

    # Final game will be dumped into the build/ directory (inside of the project dir)
    build_dir = os.path.join(namespace.project_dir, "build")
    info(f"Building game `{namespace.project_dir}`")

    # Remove the build dir if it exists
    subprocess.run(["rm", "-rf", build_dir], stdout=subprocess.PIPE)
    # Make the build dir
    subprocess.run(["mkdir", "-p", build_dir], stdout=subprocess.PIPE)
    # Copy the frontend files over
    subprocess.run(
        [
            "cp",
            os.path.join(FRONTEND_DIR, "main.css"),
            os.path.join(FRONTEND_DIR, "paignion.js"),
            build_dir,
        ],
        stdout=subprocess.PIPE,
    )

    # Put game data into the generated paignion.js file
    with open(os.path.join(build_dir, "paignion.js"), "r") as f:
        frontend_engine_data = f.read()

    # The game data object needs to be written on the top of the file, because
    # its declaration must come before any references to it
    paignion_js_data = (
        f"// Automatically generated game data object\n"
        f"let GAME_DATA = {json.dumps(GAME_DATA)};\n\n\n"
        f"{frontend_engine_data}"
    )

    # Read main.css
    with open(os.path.join(build_dir, "main.css"), "r") as f:
        main_css_data = f.read()

    # Collapse all frontend files into index.html
    with open(os.path.join(build_dir, "index.html"), "w") as f:
        f.write(INDEX_HTML_TEMPLATE.format(main_css_data, paignion_js_data))

    # Remove main.css and paignion.js
    subprocess.run(
        [
            "rm",
            os.path.join(build_dir, "main.css"),
            os.path.join(build_dir, "paignion.js"),
        ]
    )

    info(f"Done! Your game can be found at `{build_dir}/index.html`")


def paignion_main_function():
    """Handle Paignion being called from the command line."""
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
