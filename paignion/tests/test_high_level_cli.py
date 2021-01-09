import unittest
import subprocess
import sys
import os
import glob

from paignion.definitions import __version__
from paignion.tools import color_message
from paignion.exceptions import PaignionException
from paignion.__main__ import paignion_build
from argparse import Namespace


class TestHighLevelCLI(unittest.TestCase):
    def test_version(self):
        res = subprocess.run(
            [sys.executable, "-m", "paignion", "--version"],
            stdout=subprocess.PIPE,
        )

        self.assertEqual(res.stdout.decode("utf-8")[:-1], __version__)

    def test_init_without_project_dir(self):
        with open(os.devnull, "w") as stderr:
            res = subprocess.run(
                [sys.executable, "-m", "paignion", "init"],
                stderr=stderr,
            )

        self.assertEqual(res.returncode, 2)

    def test_build_without_project_dir(self):
        with open(os.devnull, "w") as stderr:
            res = subprocess.run(
                [sys.executable, "-m", "paignion", "build"],
                stderr=stderr,
            )

        self.assertEqual(res.returncode, 2)

    def test_init_with_default_project(self):
        res = subprocess.run(
            [sys.executable, "-m", "paignion", "init", "paignion/tests/default_game"],
            stdout=subprocess.PIPE,
        )

        # Make sure we got the right log message
        self.assertEqual(
            res.stdout.decode("utf-8")[:-1],
            color_message(
                "[paignion] Initialized new Paignion game at "
                "`paignion/tests/default_game`",
                color="yellow",
            ),
        )

        # Check that the project dir exists
        self.assertTrue(
            os.path.exists("paignion/tests/default_game")
            and os.path.isdir("paignion/tests/default_game")
        )

        # Check that the rooms dir exists
        self.assertTrue(
            os.path.exists("paignion/tests/default_game/rooms")
            and os.path.isdir("paignion/tests/default_game/rooms")
        )

        # Check that the room files exist
        self.assertTrue(
            (
                os.path.exists("paignion/tests/default_game/rooms/origin.md")
                and os.path.isfile("paignion/tests/default_game/rooms/origin.md")
            )
            and (
                os.path.exists("paignion/tests/default_game/rooms/second_room.md")
                and os.path.isfile("paignion/tests/default_game/rooms/second_room.md")
            )
        )

        # Clean up
        subprocess.run(["rm", "-r", "paignion/tests/default_game/"])

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
                    "paignion/tests/default_game",
                ],
                stdout=d,
            )

        # Attempt to build it
        res = subprocess.run(
            [sys.executable, "-m", "paignion", "build", "paignion/tests/default_game"],
            stdout=subprocess.PIPE,
        )

        # Make sure we got the right log message
        log_messages = res.stdout.decode("utf-8")[:-1].split("\n")
        self.assertEqual(
            log_messages[0],
            color_message(
                "[paignion] Building game `paignion/tests/default_game`", color="yellow"
            ),
        )
        self.assertEqual(
            log_messages[1],
            color_message(
                "[paignion] Done! Your game can be found at "
                "`paignion/tests/default_game/build/index.html`",
                color="yellow",
            ),
        )

        # Check that the project dir still exists
        self.assertTrue(
            os.path.exists("paignion/tests/default_game")
            and os.path.isdir("paignion/tests/default_game")
        )

        # Check that the rooms dir still exists
        self.assertTrue(
            os.path.exists("paignion/tests/default_game/rooms")
            and os.path.isdir("paignion/tests/default_game/rooms")
        )

        # Check that the room files still exist
        self.assertTrue(
            (
                os.path.exists("paignion/tests/default_game/rooms/origin.md")
                and os.path.isfile("paignion/tests/default_game/rooms/origin.md")
            )
            and (
                os.path.exists("paignion/tests/default_game/rooms/second_room.md")
                and os.path.isfile("paignion/tests/default_game/rooms/second_room.md")
            )
        )

        # Check that the build dir was created
        self.assertTrue(
            os.path.exists("paignion/tests/default_game/build")
            and os.path.isdir("paignion/tests/default_game/build")
        )

        # Check that the build dir only contains index.html
        build_files = [f for f in glob.glob("paignion/tests/default_game/build/*")]
        self.assertEqual(len(build_files), 1)
        self.assertEqual(build_files[0], "paignion/tests/default_game/build/index.html")

        # Check the content of the game that was just built
        with open("paignion/tests/default_game/build/index.html", "r") as f:
            built_game = f.read()

        with open("paignion/tests/test_data/default_game_index.html", "r") as f:
            expected_game = f.read()

        self.assertEqual(built_game, expected_game)

        # Clean up
        subprocess.run(["rm", "-r", "paignion/tests/default_game/"])

    def test_build_fail_no_rooms(self):
        # Init project first
        with open(os.devnull, "w") as d:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "paignion",
                    "init",
                    "paignion/tests/default_game",
                ],
                stdout=d,
            )

        # Remove rooms directory
        subprocess.run(["rm", "-r", "paignion/tests/default_game/rooms"])

        # Try to build, should fail
        with self.assertRaises(PaignionException):
            paignion_build(Namespace(project_dir="paignion/tests/default_game"))

        # Clean up
        subprocess.run(["rm", "-r", "paignion/tests/default_game/"])

    def test_build_fail_no_origin_room(self):
        # Init project first
        with open(os.devnull, "w") as d:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "paignion",
                    "init",
                    "paignion/tests/default_game",
                ],
                stdout=d,
            )

        # Remove the origin room
        subprocess.run(["rm", "paignion/tests/default_game/rooms/origin.md"])

        # Try to build, should fail
        with self.assertRaises(PaignionException):
            paignion_build(Namespace(project_dir="paignion/tests/default_game"))

        # Clean up
        subprocess.run(["rm", "-r", "paignion/tests/default_game/"])
