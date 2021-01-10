import pytest
import subprocess
import sys
import os
import glob

from paignion.definitions import __version__
from paignion.tools import color_message
from paignion.exceptions import PaignionException
from paignion.__main__ import paignion_build
from argparse import Namespace


class TestHighLevelCLI:
    def test_version(self):
        res = subprocess.run(
            [sys.executable, "-m", "paignion", "--version"],
            stdout=subprocess.PIPE,
        )

        assert res.stdout.decode("utf-8")[:-1] == __version__

    def test_no_arguments(self):
        res = subprocess.run(
            [sys.executable, "-m", "paignion"],
            stdout=subprocess.PIPE,
        )

        # When called with no arguments, it should print help and exit gracefully
        assert res.returncode == 0

    def test_init_without_project_dir(self):
        with open(os.devnull, "w") as stderr:
            res = subprocess.run(
                [sys.executable, "-m", "paignion", "init"],
                stderr=stderr,
            )

        assert res.returncode == 2

    def test_build_without_project_dir(self):
        with open(os.devnull, "w") as stderr:
            res = subprocess.run(
                [sys.executable, "-m", "paignion", "build"],
                stderr=stderr,
            )

        assert res.returncode == 2

    def test_init_with_default_project(self):
        res = subprocess.run(
            [sys.executable, "-m", "paignion", "init", "tests/default_game"],
            stdout=subprocess.PIPE,
        )

        # Make sure we got the right log message
        assert res.stdout.decode("utf-8")[:-1] == color_message(
            "[paignion] Initialized new Paignion game at " "`tests/default_game`",
            color="yellow",
        )

        # Check that the project dir exists
        assert os.path.exists("tests/default_game") and os.path.isdir(
            "tests/default_game"
        )

        # Check that the rooms dir exists
        assert os.path.exists("tests/default_game/rooms") and os.path.isdir(
            "tests/default_game/rooms"
        )

        # Check that the room files exist
        assert (
            os.path.exists("tests/default_game/rooms/origin.md")
            and os.path.isfile("tests/default_game/rooms/origin.md")
        ) and (
            os.path.exists("tests/default_game/rooms/second_room.md")
            and os.path.isfile("tests/default_game/rooms/second_room.md")
        )

        # Clean up
        subprocess.run(["rm", "-r", "tests/default_game/"])

    def test_build_with_default_project(self):
        self.maxDiff = None
        # Init project first
        with open(os.devnull, "w") as d:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "paignion",
                    "init",
                    "tests/default_game",
                ],
                stdout=d,
            )

        # Attempt to build it
        res = subprocess.run(
            [sys.executable, "-m", "paignion", "build", "tests/default_game"],
            stdout=subprocess.PIPE,
        )

        # Make sure we got the right log message
        log_messages = res.stdout.decode("utf-8")[:-1].split("\n")
        assert log_messages[0] == color_message(
            "[paignion] Building game `tests/default_game`", color="yellow"
        )
        assert log_messages[1] == color_message(
            "[paignion] Done! Your game can be found at "
            "`tests/default_game/build/index.html`",
            color="yellow",
        )

        # Check that the project dir still exists
        assert os.path.exists("tests/default_game") and os.path.isdir(
            "tests/default_game"
        )

        # Check that the rooms dir still exists
        assert os.path.exists("tests/default_game/rooms") and os.path.isdir(
            "tests/default_game/rooms"
        )

        # Check that the room files still exist
        assert (
            os.path.exists("tests/default_game/rooms/origin.md")
            and os.path.isfile("tests/default_game/rooms/origin.md")
        ) and (
            os.path.exists("tests/default_game/rooms/second_room.md")
            and os.path.isfile("tests/default_game/rooms/second_room.md")
        )

        # Check that the build dir was created
        assert os.path.exists("tests/default_game/build") and os.path.isdir(
            "tests/default_game/build"
        )

        # Check that the build dir only contains index.html
        build_files = [f for f in glob.glob("tests/default_game/build/*")]
        assert len(build_files) == 1
        assert build_files[0] == "tests/default_game/build/index.html"

        # Check the content of the game that was just built
        with open("tests/default_game/build/index.html", "r") as f:
            built_game = f.read()

        with open("tests/test_data/default_game_index.html", "r") as f:
            expected_game = f.read()

        assert built_game == expected_game

        # Clean up
        subprocess.run(["rm", "-r", "tests/default_game/"])

    def test_build_fail_no_rooms(self):
        # Init project first
        with open(os.devnull, "w") as d:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "paignion",
                    "init",
                    "tests/default_game",
                ],
                stdout=d,
            )

        # Remove rooms directory
        subprocess.run(["rm", "-r", "tests/default_game/rooms"])

        # Try to build, should fail
        with pytest.raises(PaignionException):
            paignion_build(Namespace(project_dir="tests/default_game"))

        # Clean up
        subprocess.run(["rm", "-r", "tests/default_game/"])

    def test_build_fail_no_origin_room(self):
        # Init project first
        with open(os.devnull, "w") as d:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "paignion",
                    "init",
                    "tests/default_game",
                ],
                stdout=d,
            )

        # Remove the origin room
        subprocess.run(["rm", "tests/default_game/rooms/origin.md"])

        # Try to build, should fail
        with pytest.raises(PaignionException):
            paignion_build(Namespace(project_dir="tests/default_game"))

        # Clean up
        subprocess.run(["rm", "-r", "tests/default_game/"])
