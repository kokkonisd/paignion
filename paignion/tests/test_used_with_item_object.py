import unittest

from paignion.used_with_item import PaignionUsedWithItem
from paignion.exceptions import PaignionUsedWithItemException


EXPECTED_DEFAULT_USED_WITH_ITEM_DUMP = """\
{
    "actions": "",
    "consumes_object": false,
    "consumes_subject": false,
    "effect_message": "test effect message",
    "name": "test name"
}\
"""


class TestUsedWithItemObject(unittest.TestCase):
    def test_used_with_item_defaults(self):
        uw_item = PaignionUsedWithItem(
            name="test name", effect_message="test effect message"
        )

        self.assertEqual(uw_item.name, "test name")
        self.assertEqual(uw_item.effect_message, "test effect message")
        self.assertEqual(uw_item.consumes_subject, False)
        self.assertEqual(uw_item.consumes_object, False)
        self.assertEqual(uw_item.actions, "")

    def test_missing_name_and_effect_message(self):
        with self.assertRaises(TypeError) as err:
            uw_item = PaignionUsedWithItem()

        self.assertEqual(
            str(err.exception),
            "__init__() missing 2 required positional arguments: 'name' and "
            "'effect_message'",
        )

        with self.assertRaises(TypeError) as err:
            uw_item = PaignionUsedWithItem(name="test name")

        self.assertEqual(
            str(err.exception),
            "__init__() missing 1 required positional argument: 'effect_message'",
        )

        with self.assertRaises(TypeError) as err:
            uw_item = PaignionUsedWithItem(effect_message="test effect message")

        self.assertEqual(
            str(err.exception),
            "__init__() missing 1 required positional argument: 'name'",
        )

        with self.assertRaises(PaignionUsedWithItemException) as err:
            uw_item = PaignionUsedWithItem(
                name=None, effect_message="test effect message"
            )

        self.assertEqual(str(err.exception), "Name missing for used_with item")

        with self.assertRaises(PaignionUsedWithItemException) as err:
            uw_item = PaignionUsedWithItem(name="test name", effect_message=None)

        self.assertEqual(
            str(err.exception), "Effect message missing for used_with item `test name`"
        )

        with self.assertRaises(PaignionUsedWithItemException) as err:
            uw_item = PaignionUsedWithItem(name=None, effect_message=None)

        self.assertEqual(str(err.exception), "Name missing for used_with item")

    def test_accepts_correct_consume_flags(self):
        uw_item = PaignionUsedWithItem(
            name="test name",
            effect_message="test effect message",
            consumes_subject=False,
            consumes_object=False,
        )
        self.assertEqual(uw_item.consumes_subject, False)
        self.assertEqual(uw_item.consumes_object, False)

        uw_item = PaignionUsedWithItem(
            name="test name",
            effect_message="test effect message",
            consumes_subject=False,
            consumes_object=True,
        )
        self.assertEqual(uw_item.consumes_subject, False)
        self.assertEqual(uw_item.consumes_object, True)

        uw_item = PaignionUsedWithItem(
            name="test name",
            effect_message="test effect message",
            consumes_subject=True,
            consumes_object=False,
        )
        self.assertEqual(uw_item.consumes_subject, True)
        self.assertEqual(uw_item.consumes_object, False)

        uw_item = PaignionUsedWithItem(
            name="test name",
            effect_message="test effect message",
            consumes_subject=True,
            consumes_object=True,
        )
        self.assertEqual(uw_item.consumes_subject, True)
        self.assertEqual(uw_item.consumes_object, True)

    def test_passing_nonlist_values_to_actions(self):
        with self.assertRaises(PaignionUsedWithItemException) as err:
            uw_item = PaignionUsedWithItem(
                name="test name", effect_message="test effect message", actions=1
            )

        self.assertEqual(
            str(err.exception),
            "Actions should be a list for used_with item `test name`",
        )

        with self.assertRaises(PaignionUsedWithItemException) as err:
            uw_item = PaignionUsedWithItem(
                name="test name",
                effect_message="test effect message",
                actions='set(west, "hidden_room", origin)',
            )

        self.assertEqual(
            str(err.exception),
            "Actions should be a list for used_with item `test name`",
        )

    def test_dump(self):
        self.maxDiff = None

        uw_item = PaignionUsedWithItem(
            name="test name", effect_message="test effect message"
        )

        self.assertEqual(str(uw_item), EXPECTED_DEFAULT_USED_WITH_ITEM_DUMP)
