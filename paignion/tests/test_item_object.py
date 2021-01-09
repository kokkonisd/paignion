import unittest

from paignion.item import PaignionItem
from paignion.used_with_item import PaignionUsedWithItem
from paignion.exceptions import PaignionItemException


EXPECTED_DEFAULT_ITEM_DUMP = """\
{
    "amount": 1,
    "description": "test description",
    "effect": null,
    "name": "test name",
    "used_with": [],
    "visible": true
}\
"""


class TestItemObject(unittest.TestCase):
    def test_item_defaults(self):
        item = PaignionItem(name="test name", description="test description")

        self.assertEqual(item.name, "test name")
        self.assertEqual(item.description, "test description")
        self.assertEqual(item.amount, 1)
        self.assertEqual(item.visible, True)
        self.assertEqual(item.effect, None)
        self.assertEqual(item.used_with, [])

    def test_missing_name_and_description(self):
        with self.assertRaises(TypeError) as err:
            item = PaignionItem()

        self.assertEqual(
            str(err.exception),
            "__init__() missing 2 required positional arguments: 'name' and "
            "'description'",
        )

        with self.assertRaises(TypeError) as err:
            item = PaignionItem(name="test name")

        self.assertEqual(
            str(err.exception),
            "__init__() missing 1 required positional argument: 'description'",
        )

        with self.assertRaises(TypeError) as err:
            item = PaignionItem(description="test description")

        self.assertEqual(
            str(err.exception),
            "__init__() missing 1 required positional argument: 'name'",
        )

        with self.assertRaises(PaignionItemException) as err:
            item = PaignionItem(name=None, description="test description")

        self.assertEqual(str(err.exception), "Name missing for item")

        with self.assertRaises(PaignionItemException) as err:
            item = PaignionItem(name="test name", description=None)

        self.assertEqual(str(err.exception), "Description missing for item `test name`")

        with self.assertRaises(PaignionItemException) as err:
            item = PaignionItem(name=None, description=None)

        self.assertEqual(str(err.exception), "Name missing for item")

    def test_accepts_integer_or_inf_amount(self):
        item = PaignionItem(name="test name", description="test description", amount=1)
        item = PaignionItem(name="test name", description="test description", amount=92)
        item = PaignionItem(
            name="test name", description="test description", amount=23.2
        )
        item = PaignionItem(
            name="test name", description="test description", amount="inf"
        )

    def test_rejects_invalid_amount(self):
        with self.assertRaises(ValueError) as err:
            item = PaignionItem(
                name="test name", description="test description", amount="abc"
            )

        self.assertEqual(
            str(err.exception), "invalid literal for int() with base 10: 'abc'"
        )

        with self.assertRaises(ValueError) as err:
            item = PaignionItem(
                name="test name", description="test description", amount="10f"
            )

        self.assertEqual(
            str(err.exception), "invalid literal for int() with base 10: '10f'"
        )

        with self.assertRaises(PaignionItemException) as err:
            item = PaignionItem(
                name="test name", description="test description", amount=0
            )

        self.assertEqual(
            str(err.exception), "Negative or zero amount for item `test name`"
        )

        with self.assertRaises(PaignionItemException) as err:
            item = PaignionItem(
                name="test name", description="test description", amount=-10
            )

        self.assertEqual(
            str(err.exception), "Negative or zero amount for item `test name`"
        )

    def test_accepts_correct_visible_flag(self):
        item = PaignionItem(
            name="test name", description="test description", visible=True
        )

        self.assertEqual(item.visible, True)

        item = PaignionItem(
            name="test name", description="test description", visible=False
        )

        self.assertEqual(item.visible, False)

    def test_passing_nonlist_values_to_used_with(self):
        with self.assertRaises(PaignionItemException) as err:
            room = PaignionItem(
                name="test name", description="test description", used_with=1
            )

        self.assertEqual(
            str(err.exception), "used_with items should be a list for item `test name`"
        )

        with self.assertRaises(PaignionItemException) as err:
            room = PaignionItem(
                name="test name",
                description="test description",
                used_with=PaignionUsedWithItem(
                    name="test used_with item",
                    effect_message="test used_with effect message",
                ),
            )

        self.assertEqual(
            str(err.exception), "used_with items should be a list for item `test name`"
        )

    def test_passing_lists_of_wrong_type_to_used_with(self):
        with self.assertRaises(PaignionItemException) as err:
            room = PaignionItem(
                name="test name", description="test description", used_with=[1, 2, 3]
            )

        self.assertEqual(
            str(err.exception),
            "used_with item `1` has incorrect type for item " "`test name`",
        )

        with self.assertRaises(PaignionItemException) as err:
            room = PaignionItem(
                name="test name",
                description="test description",
                used_with=["abc", "def", "ghi"],
            )

        self.assertEqual(
            str(err.exception),
            "used_with item `abc` has incorrect type for item " "`test name`",
        )

    def test_dump(self):
        self.maxDiff = None

        item = PaignionItem(name="test name", description="test description")

        self.assertEqual(str(item), EXPECTED_DEFAULT_ITEM_DUMP)
